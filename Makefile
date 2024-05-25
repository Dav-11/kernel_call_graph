KERNEL_VERSION	:= 6.8.0

ifeq ($(shell uname -s),Linux)
  
  # If the OS is Linux, set KERNEL_VERSION to the current kernel version
  KERNEL_VERSION := $(shell uname -r | cut -d- -f1)
endif

# Define a function to remove trailing ".0" (if needed)
ifeq ($(findstring .0,$(KERNEL_VERSION)), $(KERNEL_VERSION))
  KERNEL_VERSION_NUMBER := $(KERNEL_VERSION)
else
  KERNEL_VERSION_NUMBER := $(subst .0,,$(KERNEL_VERSION))
endif

KERNEL_VERSION_MAJOR	:= $(shell echo $(KERNEL_VERSION) | cut -d. -f1)

KERNEL_URL				:= https://cdn.kernel.org/pub/linux/kernel/v$(KERNEL_VERSION_MAJOR).x/linux-$(KERNEL_VERSION_NUMBER).tar.xz
UNTAR_DIR				:= linux-$(KERNEL_VERSION_NUMBER)
TAR_FILE				:= $(UNTAR_DIR).tar.xz

LINUX_PATH				:= $(abspath ./linux)

# hide output unless V=1
ifeq ($(V),1)
	Q =
	msg =
else
	Q = @
	msg = @printf '  %-8s %s%s\n'					\
		      "$(1)"						\
		      "$(patsubst $(abspath $(OUTPUT))/%,%,$(2))"	\
		      "$(if $(3), $(3))";
	MAKEFLAGS += --no-print-directory
endif

all: $(LINUX_PATH) cscope.files cscope.out

$(LINUX_PATH):
	$(call msg,CURL,$(KERNEL_URL))
	$(Q) curl --output $(TAR_FILE) -s $(KERNEL_URL)

	$(call msg,UNTAR,$(TAR_FILE))
	$(Q) tar -xf $(TAR_FILE)

	$(call msg,MV,$(LINUX_PATH))
	$(Q) mv $(UNTAR_DIR) $(LINUX_PATH)

	$(call msg,RM,$(TAR_FILE))
	$(Q) rm -f $(TAR_FILE)

cscope.files: $(LINUX_PATH)
	find  $(LINUX_PATH)                                                            \
		-path "$(LINUX_PATH)/arch/*" ! -path "$(LINUX_PATH)/arch/riscv*" -prune -o \
		-path "$(LINUX_PATH)/tmp*" -prune -o                                       \
		-path "$(LINUX_PATH)/Documentation*" -prune -o                             \
		-path "$(LINUX_PATH)/scripts*" -prune -o                                   \
		-path "$(LINUX_PATH)/drivers*" -prune -o                                   \
		-name "*.[chxsS]" -print > "$(LINUX_PATH)"/cscope.files

cscope.out: cscope.files
	$(call msg,CSCOPE,cscope.out)
	$(Q) cscope -b -q -k
