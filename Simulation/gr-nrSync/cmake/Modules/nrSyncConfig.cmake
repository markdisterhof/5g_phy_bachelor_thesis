INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_NRSYNC nrSync)

FIND_PATH(
    NRSYNC_INCLUDE_DIRS
    NAMES nrSync/api.h
    HINTS $ENV{NRSYNC_DIR}/include
        ${PC_NRSYNC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    NRSYNC_LIBRARIES
    NAMES gnuradio-nrSync
    HINTS $ENV{NRSYNC_DIR}/lib
        ${PC_NRSYNC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/nrSyncTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(NRSYNC DEFAULT_MSG NRSYNC_LIBRARIES NRSYNC_INCLUDE_DIRS)
MARK_AS_ADVANCED(NRSYNC_LIBRARIES NRSYNC_INCLUDE_DIRS)
