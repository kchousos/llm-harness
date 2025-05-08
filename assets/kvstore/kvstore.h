#ifndef KVSTORE_H
#define KVSTORE_H

#include <stddef.h>

void kvstore_init(void);
void kvstore_cleanup(void);
void kvstore_handle_command(const char *command);

#endif // KVSTORE_H
