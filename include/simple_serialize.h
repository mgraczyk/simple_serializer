#pragma once

#include <stdio.h>

#ifndef _sERIALIZERS_EMITTED

#define simple_serialize(TYPENAME, PTR, FP) \
    fputs(#TYPENAME, FP)

#else

#define simple_serialize(TYPENAME, PTR, FP) \
    simple_serialize_ ## TYPENAME(PTR, FP)

#endif
