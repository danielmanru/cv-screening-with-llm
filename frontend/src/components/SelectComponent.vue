<script setup lang="ts">
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "vue";

interface Item {
  value: string;
  label: string;
}

const selected = defineModel<string | null>({ default: null });
const props = defineProps<{
  title?: string;
  items?: Item[];
  class?: HTMLAttributes["class"];
}>();
</script>

<template>
  <Select v-model="selected">
    <SelectTrigger :class="cn(props.class)">
      <SelectValue :placeholder="props.title" />
    </SelectTrigger>
    <SelectContent>
      <SelectItem
        v-for="item in props.items"
        :key="item.value"
        :value="item.value"
      >
        {{ item.label }}
      </SelectItem>
    </SelectContent>
  </Select>
</template>
