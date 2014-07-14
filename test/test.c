#include "test.h"
#include "serializers.h"
#include "simple_serialize.h"

#include <stdio.h>


int main()
{
    simple_serialize(object_t, &object, stdout);
}
