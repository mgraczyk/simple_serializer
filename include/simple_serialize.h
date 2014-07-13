#pragma once

#include <stdio.h>

#ifndef _sERIALIZERS_EMITTED

#define simple_serialize(TYPENAME, PTR) \
    puts(#TYPENAME)

#else

#define simple_serialize(TYPENAME, PTR) \
    simple_serialize_ ## TYPENAME(PTR)

#endif
