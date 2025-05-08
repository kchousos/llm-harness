#include "kvstore.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_KV 10
#define MAX_KEY_LEN 32

typedef struct {
    char key[MAX_KEY_LEN];
    char *value;  // dynamically allocated
} kv_pair;

static kv_pair store[MAX_KV];
static int kv_count = 0;

void kvstore_init(void) {
    memset(store, 0, sizeof(store));
    kv_count = 0;
}

void kvstore_cleanup(void) {
    for (int i = 0; i < kv_count; i++) {
        free(store[i].value);
        store[i].value = NULL;
    }
    kv_count = 0;
}

static kv_pair *find_key(const char *key) {
    for (int i = 0; i < kv_count; i++) {
        if (strncmp(store[i].key, key, MAX_KEY_LEN) == 0)
            return &store[i];
    }
    return NULL;
}

void kvstore_handle_command(const char *command) {
    if (strncmp(command, "SET ", 4) == 0) {
        const char *kv = command + 4;
        char *eq = strchr(kv, '=');
        if (!eq) {
            printf("Invalid SET format\n");
            return;
        }

        size_t key_len = eq - kv;
        if (key_len >= MAX_KEY_LEN) {
            printf("Key too long\n");
            return;
        }

        char key[MAX_KEY_LEN];
        strncpy(key, kv, key_len);
        key[key_len] = '\0';

        const char *value = eq + 1;

        kv_pair *pair = find_key(key);
        if (!pair && kv_count < MAX_KV) {
            pair = &store[kv_count++];
            strncpy(pair->key, key, MAX_KEY_LEN - 1);
            pair->key[MAX_KEY_LEN - 1] = '\0';
        }

        if (pair) {
            free(pair->value);

	    size_t len = strlen(value);
	    pair->value = malloc(len);
	    memcpy(pair->value, value, len);
        }
    } else if (strncmp(command, "GET ", 4) == 0) {
        const char *key = command + 4;
        kv_pair *pair = find_key(key);
        if (pair && pair->value) {
            printf("Value for '%s': %s\n", pair->key, pair->value);
        } else {
            printf("Key not found: %s\n", key);
        }
    } else {
        printf("Unknown command\n");
    }
}
