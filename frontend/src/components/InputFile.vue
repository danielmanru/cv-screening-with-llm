<script setup lang="ts">
import { ref } from "vue";

const file = defineModel<File | null>({ default: null });

const props = defineProps<{
  title?: string;
  subtitle?: string;
  required?: boolean;
}>();

const fileInput = ref<HTMLInputElement | null>(null);
const isDragged = ref(false);
const error = ref<string | null>(null);

const validateFile = (newFile: File | null): boolean => {
  if (!newFile) {
    error.value = null;
    return true;
  }

  if (newFile.type !== "application/pdf") {
    error.value = "Only PDF files are allowed.";
    return false;
  }

  if (newFile.size > 1024 * 1024) {
    error.value = "File must be 1 MB or smaller.";
    return false;
  }

  error.value = null;
  return true;
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const onDragOver = () => {
  isDragged.value = true;
};

const onDragLeave = () => {
  isDragged.value = false;
};

const updateFile = (newFile: File | null) => {
  if (newFile === null) {
    file.value = null;
    error.value = null;
    return;
  }

  if (!validateFile(newFile)) {
    return;
  }

  file.value = newFile;
};

const onDrop = (event: DragEvent) => {
  isDragged.value = false;
  const files = event.dataTransfer?.files;
  if (files && files.length > 0) {
    updateFile(files[0]);
  }
};

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const files = target.files;
  if (files && files.length > 0) {
    updateFile(files[0]);
  }
};

const removeFile = (): void => {
  updateFile(null);
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};

const formatSize = (size: number): string => {
  return (size / 1024).toFixed(2) + " KB";
};
</script>

<template>
  <div class="flex flex-col gap-4 items-start">
    <div v-if="title || subtitle" class="space-y-1">
      <h2 class="text-base font-semibold text-gray-800">
        {{ title }}
      </h2>
      <p class="text-sm text-gray-600">{{ subtitle }}</p>
    </div>
    <div
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      @click="triggerFileInput"
      :class="[
        'border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition h-[250px] flex flex-col justify-center bg-white w-full',
        isDragged ? 'border-blue-500' : 'border-gray-300 hover:border-blue-400',
      ]"
    >
      <input
        type="file"
        accept="application/pdf"
        ref="fileInput"
        class="hidden"
        @change="onFileChange"
        :required="props.required"
      />

      <div v-if="!file" class="space-y-2">
        <p class="text-gray-600 font-medium">Drag & drop file here</p>
        <p class="text-sm text-gray-400">or click to select a file</p>
      </div>

      <div v-else class="space-y-2">
        <p class="text-sm font-medium text-gray-700">{{ file.name }}</p>
        <p class="text-xs text-gray-400">{{ formatSize(file.size) }}</p>
      </div>
    </div>
    <div v-if="error" class="text-sm text-red-500">{{ error }}</div>
    <button
      v-if="file"
      @click="removeFile"
      class="mt-3 text-sm text-red-500 hover:text-red-700"
      type="button"
    >
      Remove file
    </button>
  </div>
</template>

<style scoped></style>
