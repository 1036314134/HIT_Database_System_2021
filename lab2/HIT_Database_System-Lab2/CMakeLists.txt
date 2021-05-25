cmake_minimum_required(VERSION 3.19)
project(test)

set(CMAKE_CXX_STANDARD 14)

include_directories(BufMgr/src)
include_directories(BufMgr/src/exceptions)

add_executable(test
        BufMgr/src/exceptions/bad_buffer_exception.cpp
        BufMgr/src/exceptions/bad_buffer_exception.h
        BufMgr/src/exceptions/badgerdb_exception.cpp
        BufMgr/src/exceptions/badgerdb_exception.h
        BufMgr/src/exceptions/buffer_exceeded_exception.cpp
        BufMgr/src/exceptions/buffer_exceeded_exception.h
        BufMgr/src/exceptions/file_exists_exception.cpp
        BufMgr/src/exceptions/file_exists_exception.h
        BufMgr/src/exceptions/file_not_found_exception.cpp
        BufMgr/src/exceptions/file_not_found_exception.h
        BufMgr/src/exceptions/file_open_exception.cpp
        BufMgr/src/exceptions/file_open_exception.h
        BufMgr/src/exceptions/hash_already_present_exception.cpp
        BufMgr/src/exceptions/hash_already_present_exception.h
        BufMgr/src/exceptions/hash_not_found_exception.cpp
        BufMgr/src/exceptions/hash_not_found_exception.h
        BufMgr/src/exceptions/hash_table_exception.cpp
        BufMgr/src/exceptions/hash_table_exception.h
        BufMgr/src/exceptions/insufficient_space_exception.cpp
        BufMgr/src/exceptions/insufficient_space_exception.h
        BufMgr/src/exceptions/invalid_page_exception.cpp
        BufMgr/src/exceptions/invalid_page_exception.h
        BufMgr/src/exceptions/invalid_record_exception.cpp
        BufMgr/src/exceptions/invalid_record_exception.h
        BufMgr/src/exceptions/invalid_slot_exception.cpp
        BufMgr/src/exceptions/invalid_slot_exception.h
        BufMgr/src/exceptions/page_not_pinned_exception.cpp
        BufMgr/src/exceptions/page_not_pinned_exception.h
        BufMgr/src/exceptions/page_pinned_exception.cpp
        BufMgr/src/exceptions/page_pinned_exception.h
        BufMgr/src/exceptions/slot_in_use_exception.cpp
        BufMgr/src/exceptions/slot_in_use_exception.h
        BufMgr/src/buffer.cpp
        BufMgr/src/buffer.h
        BufMgr/src/bufHashTbl.cpp
        BufMgr/src/bufHashTbl.h
        BufMgr/src/file.cpp
        BufMgr/src/file.h
        BufMgr/src/file_iterator.h
        BufMgr/src/main.cpp
        BufMgr/src/main.hpp
        BufMgr/src/page.cpp
        BufMgr/src/page.h
        BufMgr/src/page_iterator.h
        BufMgr/src/types.h)
