INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_NR_SYNC nr_sync)

FIND_PATH(
    NR_SYNC_INCLUDE_DIRS
    NAMES nr_sync/api.h
    HINTS $ENV{NR_SYNC_DIR}/include
        ${PC_NR_SYNC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    NR_SYNC_LIBRARIES
    NAMES gnuradio-nr_sync
    HINTS $ENV{NR_SYNC_DIR}/lib
        ${PC_NR_SYNC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/nr_syncTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(NR_SYNC DEFAULT_MSG NR_SYNC_LIBRARIES NR_SYNC_INCLUDE_DIRS)
MARK_AS_ADVANCED(NR_SYNC_LIBRARIES NR_SYNC_INCLUDE_DIRS)
