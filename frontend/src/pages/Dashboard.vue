<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import InputFile from "@/components/InputFile.vue";
import { Button } from "@/components/ui/button";
import {
  Astroid,
  CircleAlert,
  CircleCheck,
  RefreshCw,
  TriangleAlert,
} from "@lucide/vue";
import { Label } from "reka-ui";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";
import SelectComponent from "@/components/SelectComponent.vue";
import axiosClient from "@/axios";
import { useWebSocket } from "@vueuse/core";

const cvFile = ref<File | null>(null);
const ringRadius = 45;
const ringCircumference = 2 * Math.PI * ringRadius;
const ringOffset = computed(
  () =>
    ringCircumference *
    (1 -
      Math.min(100, Math.max(0, screening.value?.result?.match_score ?? 0)) /
        100),
);

const employmentTypeOptions = [
  { value: "fulltime", label: "Full-time" },
  { value: "parttime", label: "Part-time" },
  { value: "contract", label: "Contract" },
  { value: "internship", label: "Internship" },
];

const workArrangementOptions = [
  { value: "onsite", label: "On-site" },
  { value: "remote", label: "Remote" },
  { value: "hybrid", label: "Hybrid" },
];

const form = ref({
  name: "",
  email: "",
  jobTitle: "",
  jobRequirement: "",
  employmentType: "",
  workArrangement: "",
});

const loading = ref<Boolean>(false);

export interface jobInfo {
  job_title: string;
  employment_type: string;
  work_arrangement: string;
}

export interface ScreeningResult {
  match_score: number;
  summary: string;
  matched_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
  recommendation: string;
}

export interface Screening {
  _id: string;
  candidate_name: string;
  candidate_email: string;
  job: jobInfo;
  cv_file: null | string;
  result: ScreeningResult;
  status: string;
  error_message: null | string;
  created_at: string;
  uploaded_at: string;
}

const screening = ref<Screening | null>(null);

const submit = async () => {
  try {
    loading.value = true;
    const formData = new FormData();
    if (cvFile.value) {
      formData.append("cv", cvFile.value);
    }
    formData.append("candidate_name", form.value.name);
    formData.append("candidate_email", form.value.email);
    formData.append("job_title", form.value.jobTitle);
    formData.append("job_requirement", form.value.jobRequirement);
    formData.append("employment_type", form.value.employmentType);
    formData.append("work_arrangement", form.value.workArrangement);

    const response = await axiosClient.post("/cv-screening", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    screening.value = response.data;
  } catch (error) {
    console.error("Error submitting form:", error);
  }
};

const getScreening = async () => {
  try {
    loading.value = true;
    const response = await axiosClient.get(
      `/cv-screening/${screening.value?._id}`,
    );
    screening.value = response.data;
  } catch (error) {
    console.error("Error fetching screening result:", error);
  } finally {
    loading.value = false;
  }
};

const { status } = useWebSocket(import.meta.env.VITE_WEBSOCKET_URL, {
  autoReconnect: true,
  onMessage(ws, event) {
    if (event.data === "REFRESH_DATA") {
      getScreening();
    }
  },
});
</script>

<template>
  <div class="w-full mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 gap-6 xl:grid-cols-10">
      <div class="xl:col-span-4 flex flex-col gap-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 mb-4">
            Candidate Analysis
          </h1>
        </div>
        <form @submit.prevent="submit" class="flex flex-col gap-6">
          <InputFile
            v-model="cvFile"
            title="Candidate CV"
            subtitle="Upload a CV file to analyze the candidate's qualifications and skills."
            :required="true"
          />
          <div class="flex flex-col gap-2">
            <Label class="text-sm text-gray-600">Name</Label>
            <Input
              placeholder="Enter candidate's name"
              class="w-full bg-white"
              type="text"
              required
              v-model="form.name"
            />
          </div>
          <div class="flex flex-col gap-2">
            <Label class="text-sm text-gray-600">Email</Label>
            <Input
              placeholder="Enter candidate's email"
              class="w-full bg-white"
              type="email"
              required
              v-model="form.email"
            />
          </div>
          <div class="flex flex-col gap-2">
            <Label class="text-sm text-gray-600">Job Requirements</Label>
            <Textarea
              placeholder="Paste the job description here"
              class="bg-white min-h-[150px]"
              required
              v-model="form.jobRequirement"
            />
          </div>
          <div class="flex flex-col gap-2">
            <Label class="text-sm text-gray-600">Job Title</Label>
            <Input
              placeholder="Enter the job title"
              class="w-full bg-white"
              type="text"
              required
              v-model="form.jobTitle"
            />
          </div>
          <div class="flex flex-col gap-2">
            <Label class="text-sm text-gray-600">Employment Type</Label>
            <SelectComponent
              class="bg-white w-full"
              v-model="form.employmentType"
              title="Select Employment Type"
              :items="employmentTypeOptions"
              requried
            />
          </div>
          <div class="flex flex-col gap-2">
            <Label class="text-sm text-gray-600">Work Arrangement</Label>
            <SelectComponent
              class="bg-white w-full"
              title="Select Work Arrangement"
              v-model="form.workArrangement"
              :items="workArrangementOptions"
              requried
            />
          </div>
          <div class="flex w-full justify-center">
            <Button
              type="submit"
              class="bg-[#5248E9] w-full sm:w-[50%] p-6 hover:cursor-pointer hover:bg-[#413bb8]"
              :disabled="loading"
            >
              <RefreshCw
                v-if="loading"
                role="status"
                aria-label="Loading"
                class="size-5 animate-spin"
              />
              <p>Analyze Candidate</p></Button
            >
          </div>
        </form>
      </div>
      <div class="xl:col-span-6 flex flex-col gap-6" v-if="loading">
        <div class="flex justify-between">
          <h1 class="text-2xl font-bold text-gray-800 mb-4">
            Analysis Results
          </h1>
          <div
            class="bg-gray-300 animate-pulse rounded-[999px] h-fit px-2 py-1 justify-center items-center flex"
          >
            <p class="text-gray-700 font-medium">Analyzing...</p>
          </div>
        </div>
        <div
          class="p-2 border borde-1 border-gray-300 rounded-[8px] w-fit flex justify-center items-center gap-2 bg-[#E4E8FF] mx-auto animate-pulse"
        >
          <CircleAlert class="size-5 text-blue-500" />
          <p class="text-blue-500 text-center">
            Please wait, AI is analyzing the candidate's fit for the job
          </p>
        </div>
        <div class="flex flex-col gap-1 w-full items-center">
          <Skeleton class="h-4 w-[250px] bg-[#E4E8FF]" />
          <Skeleton class="h-4 w-[350px] bg-[#E4E8FF]" />
        </div>
        <div class="grid grid-cols-1 gap-2 md:grid-cols-10">
          <div
            class="md:col-span-4 flex flex-col gap-4 animate-pulse w-full items-center bg-white rounded-[8px] p-8 shadow-sm justify-center"
          >
            <p class="text-sm text-gray-500">Match Score</p>
            <Skeleton class="h-4 w-[150px] h-[150px] bg-[#E4E8FF]" />
          </div>
          <div
            class="md:col-span-6 flex flex-col gap-4 w-full items-center bg-white rounded-[8px] p-8 shadow-sm animate-pulse"
          >
            <div class="flex justify-start items-center gap-4 w-full">
              <Astroid class="size-6 text-[#5446D7]" />
              <h2 class="text-xl font-semibold text-gray-700">Summary</h2>
            </div>
            <div class="flex justify-start flex-col w-full gap-2">
              <Skeleton class="h-4 w-[250px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[300px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[200px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[250px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[300px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[200px] bg-[#E4E8FF]" />
            </div>
          </div>
        </div>
        <div class="grid grid-cols-1 gap-2 md:grid-cols-10">
          <div
            class="md:col-span-5 border-l-4 border-[#1E6C48]/60 rounded-lg bg-white p-4 shadow-sm animate-pulse"
          >
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <span><CircleCheck class="size-6 text-[#1E6C48]" /></span>
              <p class="text-lg font-semibold text-gray-700">Strengths</p>
            </h3>
            <ul class="mt-3 space-y-2">
              <Skeleton class="h-4 w-[250px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[300px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[350px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[200px] bg-[#E4E8FF]" />
            </ul>
          </div>
          <div
            class="md:col-span-5 border-l-4 border-[#654000]/60 rounded-lg bg-white p-4 shadow-sm animate-pulse"
          >
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <span><TriangleAlert class="size-6 text-[#654000]" /></span>
              <p class="text-lg font-semibold text-gray-700">Gaps</p>
            </h3>
            <ul class="mt-3 space-y-2">
              <Skeleton class="h-4 w-[250px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[300px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[350px] bg-[#E4E8FF]" />
              <Skeleton class="h-4 w-[200px] bg-[#E4E8FF]" />
            </ul>
          </div>
        </div>
      </div>
      <div
        class="xl:col-span-6 flex flex-col gap-6"
        v-if="screening?.status === 'completed'"
      >
        <div class="flex justify-between">
          <h1 class="text-2xl font-bold text-gray-800 mb-4">
            Analysis Results
          </h1>
          <div
            :class="[
              'rounded-[999px] h-fit px-2 py-1 justify-center items-center flex',
              screening?.result?.recommendation === 'Highly Suitable'
                ? 'bg-emerald-100 text-emerald-800'
                : screening?.result?.recommendation === 'Suitable'
                  ? 'bg-amber-100 text-amber-800'
                  : screening?.result?.recommendation === 'Consider'
                    ? 'bg-orange-100 text-orange-800'
                    : 'bg-gray-100 text-gray-700',
            ]"
          >
            <p class="font-bold">
              {{ screening?.result?.recommendation }}
            </p>
          </div>
        </div>
        <div class="flex flex-col gap-1 w-full items-center">
          <h2 class="text-lg font-semibold text-gray-700">
            {{ screening?.candidate_name }}
          </h2>
          <p class="text-gray-600 text-center">
            {{ screening?.candidate_email }}
          </p>
        </div>
        <div class="grid grid-cols-1 gap-2 md:grid-cols-10">
          <div
            class="md:col-span-4 flex flex-col gap-4 w-full items-center bg-white rounded-[8px] p-8 shadow-sm justify-center"
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
                  screening?.result?.match_score ?? 0
                }}</span>
                <span class="text-sm text-gray-500">/ 100</span>
              </div>
            </div>
          </div>
          <div
            class="md:col-span-6 flex flex-col gap-4 w-full items-center bg-white rounded-[8px] p-8 shadow-sm"
          >
            <div class="flex justify-start items-center gap-4 w-full">
              <Astroid class="size-6 text-[#5446D7]" />
              <h2 class="text-xl font-semibold text-gray-700">Summary</h2>
            </div>
            <p class="text-gray-600">
              {{ screening?.result?.summary }}
            </p>
          </div>
        </div>
        <div class="grid grid-cols-1 gap-2 md:grid-cols-10">
          <div
            class="md:col-span-5 border-l-4 border-[#1E6C48] rounded-lg bg-white p-4 shadow-sm"
          >
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <span
                ><CircleCheck class="size-6 fill-[#1E6C48] text-white"
              /></span>
              <p class="text-lg font-semibold text-gray-700">Strengths</p>
            </h3>
            <ul class="mt-3 space-y-2">
              <li
                v-for="strength in screening?.result?.strengths"
                :key="strength"
                class="flex items-start gap-2 text-gray-600"
              >
                <span class="text-[#1E6C48] mt-0.5">✓</span>
                {{ strength }}
              </li>
            </ul>
          </div>
          <div
            class="md:col-span-5 border-l-4 border-[#654000] rounded-lg bg-white p-4 shadow-sm"
          >
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <span
                ><TriangleAlert class="size-6 fill-[#654000] text-white"
              /></span>
              <p class="text-lg font-semibold text-gray-700">Gaps</p>
            </h3>
            <ul class="mt-3 space-y-2">
              <li
                v-for="weakness in screening?.result?.weaknesses"
                :key="weakness"
                class="flex items-start gap-2 text-gray-600"
              >
                <span class="text-[#654000] mt-0.5">–</span>
                {{ weakness }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
