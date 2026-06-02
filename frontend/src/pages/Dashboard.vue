<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import InputFile from "@/components/InputFile.vue";
import { Button } from "@/components/ui/button";
import { Astroid, CircleCheck, TriangleAlert } from "@lucide/vue";
import { Label } from "reka-ui";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

const cvFile = ref<File | null>(null);
const jobRequirementFile = ref<File | null>(null);
const cvScore = ref<number>(0);
const ringRadius = 45;
const ringCircumference = 2 * Math.PI * ringRadius;
const ringOffset = computed(
  () =>
    ringCircumference * (1 - Math.min(100, Math.max(0, cvScore.value)) / 100),
);

onMounted(() => {
  setTimeout(() => {
    cvScore.value = 85;
  }, 200);
});
</script>

<template>
  <div class="w-full mx-auto">
    <div class="grid grid-cols-10 gap-6">
      <div class="col-span-4 flex flex-col gap-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 mb-4">
            Candidate Analysis
          </h1>
        </div>

        <InputFile
          v-model="cvFile"
          title="Candidate CV"
          subtitle="Upload a CV file to analyze the candidate's qualifications and skills."
        />
        <div class="flex flex-col gap-2">
          <Label class="text-sm text-gray-600">Name</Label>
          <Input
            placeholder="Enter candidate's name"
            class="w-full bg-white"
            type="text"
          />
        </div>
        <div class="flex flex-col gap-2">
          <Label class="text-sm text-gray-600">Email</Label>
          <Input
            placeholder="Enter candidate's email"
            class="w-full bg-white"
            type="email"
          />
        </div>
        <div class="flex flex-col gap-2">
          <Label class="text-sm text-gray-600">Job Requirements</Label>
          <Textarea
            placeholder="Paste the job description here"
            class="bg-white min-h-[150px]"
          />
        </div>
        <div class="flex w-full justify-center">
          <Button
            class="bg-[#5248E9] w-[50%] p-6 hover:cursor-pointer hover:bg-[#413bb8]"
          >
            Analyze Candidate
          </Button>
        </div>
      </div>

      <div class="col-span-6 flex flex-col gap-6">
        <div class="flex justify-between">
          <h1 class="text-2xl font-bold text-gray-800 mb-4">
            Analysis Results
          </h1>
          <div
            class="bg-[#81F8B9] rounded-[999px] h-fit px-2 py-1 justify-center items-center flex"
          >
            <p class="text-gray-700 font-bold">High Match</p>
          </div>
        </div>
        <div class="flex flex-col gap-1 w-full items-center">
          <h2 class="text-lg font-semibold text-gray-700">Alex Thompson</h2>
          <p class="text-gray-600 text-center">alexthompson@gmail.com</p>
        </div>
        <div class="grid grid-cols-10 gap-2">
          <!-- analysis score -->
          <div
            class="col-span-4 flex flex-col gap-4 w-full items-center bg-white rounded-[8px] p-8 shadow-sm justify-center"
          >
            <p class="text-sm text-gray-500">Match Score</p>
            <div class="relative flex items-center justify-center h-40 w-40">
              <svg class="h-40 w-40 -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  stroke-width="10"
                  fill="none"
                  class="text-gray-200"
                  stroke="currentColor"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  stroke-width="10"
                  fill="none"
                  class="text-[#1E6C48] transition-all duration-1000 ease-out"
                  stroke="currentColor"
                  stroke-linecap="round"
                  :stroke-dasharray="ringCircumference"
                  :stroke-dashoffset="ringOffset"
                />
              </svg>
              <div
                class="absolute inset-0 flex flex-col items-center justify-center"
              >
                <span class="text-3xl font-bold text-[gray-800]">{{
                  cvScore
                }}</span>
                <span class="text-sm text-gray-500">/ 100</span>
              </div>
            </div>
          </div>
          <div
            class="col-span-6 flex flex-col gap-4 w-full items-center bg-white rounded-[8px] p-8 shadow-sm"
          >
            <div class="flex justify-start items-center gap-4 w-full">
              <Astroid class="size-6 text-[#5446D7]" />
              <h2 class="text-xl font-semibold text-gray-700">Summary</h2>
            </div>
            <p class="text-gray-600">
              Alex Thompson has a strong match with the job requirements. His
              experience and skills align well with the position. He has
              demonstrated expertise in relevant technologies and has a proven
              track record of success in similar roles. Overall, Alex is a
              highly qualified candidate for the position. His strong match
              score indicates that he is likely to be a great fit for the role
              and could contribute significantly to the team.
            </p>
          </div>
        </div>
        <div class="grid grid-cols-10 gap-2">
          <div
            class="col-span-5 border-l-4 border-[#1E6C48] rounded-lg bg-white p-4 shadow-sm"
          >
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <span
                ><CircleCheck class="size-6 fill-[#1E6C48] text-white"
              /></span>
              <p class="text-lg font-semibold text-gray-700">Strengths</p>
            </h3>
            <ul class="mt-3 space-y-2">
              <li class="flex items-start gap-2 text-gray-600">
                <span class="text-[#1E6C48] mt-0.5">✓</span>
                Expert Vue 3 Composition API knowledge
              </li>
              <li class="flex items-start gap-2 text-gray-600">
                <span class="text-[#1E6C48] mt-0.5">✓</span>
                Strong background in frontend development
              </li>
              <li class="flex items-start gap-2 text-gray-600">
                <span class="text-[#1E6C48] mt-0.5">✓</span>
                Experience with Tailwind CSS and modern UI design principles
              </li>
            </ul>
          </div>
          <div
            class="col-span-5 border-l-4 border-[#654000] rounded-lg bg-white p-4 shadow-sm"
          >
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <span
                ><TriangleAlert class="size-6 fill-[#654000] text-white"
              /></span>
              <p class="text-lg font-semibold text-gray-700">Gaps</p>
            </h3>
            <ul class="mt-3 space-y-2">
              <li class="flex items-start gap-2 text-gray-600">
                <span class="text-[#654000] mt-0.5">–</span>
                Limited exposure to Rust/WebAssembly
              </li>
              <li class="flex items-start gap-2 text-gray-600">
                <span class="text-[#654000] mt-0.5">–</span>
                No prior experience with AI/ML projects
              </li>
              <li class="flex items-start gap-2 text-gray-600">
                <span class="text-[#654000] mt-0.5">–</span>
                Some gaps in backend development experience
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
