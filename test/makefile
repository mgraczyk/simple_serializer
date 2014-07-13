SHELL=bash
TARGET=./test
SER_HEADER=serializers.h
LIBS=
CC:=gcc
CFLAGS:=-std=c11 -Wall -fpic -O3

TEST_INPUT_DIR?=.

INCLUDE:= ../include $(TEST_INPUT_DIR)

OBJECTS = $(patsubst %.cpp, %.o, $(wildcard *.cpp)) \
          $(patsubst %.c, %.o, $(wildcard *.c)) 

HEADERS = $(wildcard *.h)
INCLUDECC = $(addprefix -I,$(INCLUDE))

.PHONY: default disasm all clean self_test serializers
.PRECIOUS: $(TARGET) $(OBJECTS)
.SUFFIXES:

default: $(TARGET)
disasm: $(TARGET).s
all: default

debug: CFLAGS+= -g -ggdb3
debug: default

%.o: %.c $(HEADERS)
	$(CC) $(INCLUDECC) $(CFLAGS) -c $< $(LIBS) -o $@

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -Wall $(LIBS) -o $@

serializers: $(SER_HEADER)
$(SER_HEADER): debug
	../src/gen_serializers.py $(TARGET) $@

run: $(TARGET)
	$(TARGET)

self_test: serializers
	@$(MAKE) -B serializers
	@$(MAKE) -B
	@diff <($(TARGET)) $(TEST_INPUT_DIR)/expected.json
	@echo PASS

%.s: %
	objdump -D -S $< > $@

clean:
	-rm -f *.o
	-rm -f $(TARGET) $(TARGET).s
