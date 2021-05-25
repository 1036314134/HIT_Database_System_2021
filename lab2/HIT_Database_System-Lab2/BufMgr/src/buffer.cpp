/**
 * @author See Contributors.txt for code contributors and overview of BadgerDB.
 *
 * @section LICENSE
 * Copyright (c) 2012 Database Group, Computer Sciences Department, University of Wisconsin-Madison.
 */

#include <memory>
#include <iostream>
#include "buffer.h"
#include "exceptions/buffer_exceeded_exception.h"
#include "exceptions/page_not_pinned_exception.h"
#include "exceptions/page_pinned_exception.h"
#include "exceptions/bad_buffer_exception.h"
#include "exceptions/hash_not_found_exception.h"

namespace badgerdb
{
    using namespace std;

    BufMgr::BufMgr(std::uint32_t bufs)
        : numBufs(bufs)
    {
        bufDescTable = new BufDesc[bufs];

        for (FrameId i = 0; i < bufs; i++)
        {
            bufDescTable[i].frameNo = i;
            bufDescTable[i].valid = false;
        }

        bufPool = new Page[bufs];

        int htsize = ((((int)(bufs * 1.2)) * 2) / 2) + 1;
        hashTable = new BufHashTbl(htsize);
        clockHand = bufs - 1;
    }

    BufMgr::~BufMgr(){//清除所有脏页并释放缓冲池和BufDesc表。
        delete hashTable;
        delete[] bufPool;
        delete[] bufDescTable;
    }

    void BufMgr::advanceClock(){//将时钟提前到缓冲池中的下一帧。
        clockHand++;
        if (clockHand >= numBufs){//取模
            clockHand %= numBufs;
        }
    }

    void BufMgr::allocBuf(FrameId &frame){
        unsigned pinned = 0;
        while (true){
            advanceClock();
            if (!bufDescTable[clockHand].valid){
                frame = clockHand;
                return;
            }
            if (bufDescTable[clockHand].refbit){
                bufDescTable[clockHand].refbit = false;
                continue;
            }
            //判断页面是否被锁定
            if (bufDescTable[clockHand].pinCnt){
                //被锁定
                pinned++;
                if (pinned == numBufs){
                    throw BufferExceededException();
                }else{
                    continue;
                }
            }
            if (bufDescTable[clockHand].dirty){
                bufDescTable[clockHand].file->writePage(bufPool[clockHand]);
                bufDescTable[clockHand].dirty = false;
            }
            //不是脏页，分配
            frame = clockHand;
            if (bufDescTable[clockHand].valid){
                //移除哈希表
                try{
                    hashTable->remove(bufDescTable[clockHand].file, bufDescTable[clockHand].pageNo);
                }
                catch (HashNotFoundException &){
                    //不在表中
                }
            }
            break;
        }
    }

    void BufMgr::readPage(File *file, const PageId pageNo, Page *&page){
        FrameId frame;
        try{
            hashTable->lookup(file, pageNo, frame);
            //页面在缓冲池中
            bufDescTable[frame].refbit = true;
            bufDescTable[frame].pinCnt++;
            page = (bufPool + frame);
        }catch (HashNotFoundException &){
            //页面不在缓冲池中
            allocBuf(frame);
            //将页面读取到缓冲池中
            bufPool[frame] = file->readPage(pageNo);
            //插入哈希表
            hashTable->insert(file, pageNo, frame);
            //调用set
            bufDescTable[frame].Set(file, pageNo);
            page = (bufPool + frame);
        }
    }

    void BufMgr::unPinPage(File *file, const PageId pageNo, const bool dirty){
        FrameId frame;
        try{
            hashTable->lookup(file, pageNo, frame);
        }catch (HashNotFoundException &){
            //没有该页面
            cerr << "Warning: unpinning a nonexistent page" << endl;
            return;
        }
        //找到页面
        if (bufDescTable[frame].pinCnt > 0){
            bufDescTable[frame].pinCnt--;
            if (dirty){
                bufDescTable[frame].dirty = true;
            }
        }else{
            //pin = 0,抛出异常
            throw PageNotPinnedException(bufDescTable[frame].file->filename(), bufDescTable[frame].pageNo, frame);
        }
    }

    void BufMgr::flushFile(const File *file){
        //扫描文件当中的所有页面
        for (FrameId fi = 0; fi < numBufs; fi++){
            if (bufDescTable[fi].file == file){
                if (!bufDescTable[fi].valid){
                    //不可用页面，抛出异常
                    throw BadBufferException(fi, bufDescTable[fi].dirty, bufDescTable[fi].valid, bufDescTable[fi].refbit);
                }
                if (bufDescTable[fi].pinCnt > 0){
                    //页面被锁定，抛出异常
                    throw PagePinnedException(file->filename(), bufDescTable[fi].pageNo, fi);
                }
                if (bufDescTable[fi].dirty){
                    //写下这一页面
                    bufDescTable[fi].file->writePage(bufPool[fi]);
                    bufDescTable[fi].dirty = false;
                }
                //从哈希表中移除页面
                hashTable->remove(file, bufDescTable[fi].pageNo);
                //清空页面
                bufDescTable[fi].Clear();
            }
        }
    }

    void BufMgr::allocPage(File *file, PageId &pageNo, Page *&page){
        //分配一个新页面并分配一个帧
        FrameId frame;
        Page p = file->allocatePage();
        allocBuf(frame);
        bufPool[frame] = p;
        pageNo = p.page_number();
        hashTable->insert(file, pageNo, frame);
        bufDescTable[frame].Set(file, pageNo);
        page = bufPool + frame;
    }

    void BufMgr::disposePage(File *file, const PageId PageNo){//删除特定页面
        FrameId frame;
        try{//如果在缓冲里，要把缓冲内容也删除
            hashTable->lookup(file, PageNo, frame);
            //移出哈希表
            hashTable->remove(file, PageNo);
            //释放
            bufDescTable[frame].Clear();
        }catch (HashNotFoundException &){
            //不在表中
        }
        //删除页面
        file->deletePage(PageNo);
    }

    void BufMgr::printSelf(void){
        BufDesc *tmpbuf;
        int validFrames = 0;

        for (unsigned i = 0; i < numBufs; i++){
            tmpbuf = &(bufDescTable[i]);
            cout << "FrameNo:" << i << " ";
            tmpbuf->Print();

            if (tmpbuf->valid == true)
                validFrames++;
        }
        cout << "Total Number of Valid Frames:" << validFrames << endl;
    }
} // namespace badgerdb
