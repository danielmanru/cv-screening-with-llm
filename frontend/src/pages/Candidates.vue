<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { UserRoundPlus } from "@lucide/vue";
import DataTable from "datatables.net-vue3";
import DataTablesCore from "datatables.net-dt";
import "datatables.net-dt/css/dataTables.dataTables.css";
import type { Screening } from "./Dashboard.vue";
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import axiosClient from "@/axios.ts";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Astroid, CircleCheck, TriangleAlert } from "@lucide/vue";
import { VisuallyHidden } from "reka-ui";

DataTable.use(DataTablesCore);

const screenings = ref<Screening[] | null>(null);
const screeningIdx = ref<number | null>(null);

const ringRadius = 45;
const ringCircumference = 2 * Math.PI * ringRadius;
const ringOffset = computed(
  () =>
    ringCircumference *
    (1 -
      Math.min(
        100,
        Math.max(
          0,
          screenings.value?.[screeningIdx.value ?? 0]?.result?.match_score ?? 0,
        ),
      ) /
        100),
);
const sheetOpen = ref<boolean>(false);
const columns = [
  {
    data: "candidate_name",
    title: "Candidate Name",
  },
  {
    data: "candidate_email",
    title: "Candidate Email",
  },
  {
    data: null,
    title: "Job",
    render: function (_data: unknown, _type: unknown, row: any) {
      return `
        <div class="flex flex-col">
          <p class="font-medium text-gray-900">
            ${row.job.title}
          </p>
          <div class="flex space-x-[5px] w-full items-center">
            <p class="text-sm text-gray-500">
              ${row.job.work_arrangement}
            </p>
            <span class="bg-gray-500 rounded-full px-[3px] py-[3px] h-fit">
            </span>
            <p class="text-sm text-gray-500">
              ${row.job.employment_type}
            </p>
          </div>
        </div>
      `;
    },
  },
  {
    data: null,
    title: "Match Score",
    type: "string",
    render: function (_data: unknown, _type: unknown, row: any) {
      const score = Math.min(100, Math.max(0, row.result?.match_score ?? 0));
      const radius = 45;
      const ringCircumference = 2 * Math.PI * radius;
      const strokeDashoffset = ringCircumference * (1 - score / 100);

      return `
      <div class="relative flex items-center justify-center h-12 w-12 mx-auto">
        <svg class="h-12 w-12 -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="${radius}"
            stroke-width="10"
            fill="none"
            stroke="#e5e7eb"
          ></circle>

          <circle
            cx="50"
            cy="50"
            r="${radius}"
            stroke-width="10"
            fill="none"
            stroke="#1E6C48"
            stroke-linecap="round"
            stroke-dasharray="${ringCircumference}"
            stroke-dashoffset="${strokeDashoffset}"
          ></circle>
        </svg>

        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-[10px] font-bold text-gray-800">
            ${score}%
          </span>
        </div>
      </div>
    `;
    },
  },
  {
    data: null,
    title: "Action",
    render: function (_data: unknown, _type: unknown, row: any, meta: any) {
      return `
        <div class="btn-view-details cursor-pointer" data-id="${meta.row}">
          <p>View Details</p>
        </div>
      `;
    },
  },
];

const options = {
  drawCallback: function () {
    document.querySelectorAll(".btn-view-details").forEach((el) => {
      el.addEventListener("click", () => {
        const id = el.getAttribute("data-id");
        screeningIdx.value = Number(id);
        sheetOpen.value = true;
      });
    });
  },
};

onMounted(async () => {
  try {
    const response = await axiosClient.get("/cv-screening");

    screenings.value = response.data;
  } catch (error) {
    console.error("Error fetching screenings:", error);
  }
});
</script>

<template>
  <div
    class="w-full h-fit flex flex-col gap-4 md:flex-row md:items-end md:justify-between"
  >
    <div class="space-y-1">
      <h1 class="text-2xl font-bold">Candidates</h1>
      <p class="text-gray-600">
        {{ `Review ${screenings?.length || 0} applicants` }}
      </p>
    </div>
    <div class="flex h-full items-end">
      <RouterLink to="/dashboard">
        <Button
          class="bg-[#3525CD] hover:bg-[#3525CD]/80 hover:cursor-pointer text-white"
        >
          <UserRoundPlus class="size-4" />
          <p>Add Candidate</p>
        </Button>
      </RouterLink>
    </div>
  </div>
  <Sheet v-model:open="sheetOpen">
    <SheetContent class="max-w-full sm:max-w-[50vw] overflow-y-auto">
      <VisuallyHidden>
        <SheetTitle>Analysis Results</SheetTitle>
        <SheetDescription>Candidate Screening Result</SheetDescription>
      </VisuallyHidden>
      <div
        class="flex flex-col gap-6 p-10"
        v-if="
          screenings &&
          screeningIdx !== null &&
          screenings[screeningIdx].status === 'completed'
        "
      >
        <div class="flex justify-between">
          <h1 class="text-2xl font-bold text-gray-800 mb-4">
            Analysis Results
          </h1>
          <div
            :class="[
              'rounded-[999px] h-fit px-2 py-1 justify-center items-center flex',
              screenings[screeningIdx].result.recommendation ===
              'Highly Suitable'
                ? 'bg-emerald-100 text-emerald-800'
                : screenings[screeningIdx].result.recommendation === 'Suitable'
                  ? 'bg-amber-100 text-amber-800'
                  : screenings[screeningIdx].result.recommendation ===
                      'Consider'
                    ? 'bg-orange-100 text-orange-800'
                    : 'bg-gray-100 text-gray-700',
            ]"
          >
            <p class="font-bold">
              {{ screenings[screeningIdx].result.recommendation }}
            </p>
          </div>
        </div>
        <div class="flex flex-col gap-1 w-full items-center">
          <h2 class="text-lg font-semibold text-gray-700">
            {{ screenings[screeningIdx].candidate_name }}
          </h2>
          <p class="text-gray-600 text-center">
            {{ screenings[screeningIdx].candidate_email }}
          </p>
        </div>
        <div class="grid grid-cols-1 gap-2 md:grid-cols-10">
          <div
            class="md:col-span-4 flex flex-col gap-4 w-full items-center bg-white rounded-[8px] p-8 justify-center"
          >
            <p class="text-sm text-gray-500">Match Score</p>
            <div
              class="relative flex items-center justify-center h-32 w-32 sm:h-40 sm:w-40"
            >
              <svg
                class="h-32 w-32 sm:h-40 sm:w-40 -rotate-90"
                viewBox="0 0 100 100"
              >
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
                  screenings[screeningIdx].result.match_score ?? 0
                }}</span>
                <span class="text-sm text-gray-500">/ 100</span>
              </div>
            </div>
          </div>
          <div
            class="md:col-span-6 flex flex-col gap-4 w-full items-center bg-white rounded-[8px] p-8"
          >
            <div class="flex justify-start items-center gap-4 w-full">
              <Astroid class="size-6 text-[#5446D7]" />
              <h2 class="text-xl font-semibold text-gray-700">Summary</h2>
            </div>
            <p class="text-gray-600">
              {{ screenings[screeningIdx].result.summary }}
            </p>
          </div>
        </div>
        <div class="grid grid-cols-1 gap-2 md:grid-cols-10">
          <div
            class="md:col-span-5 border-l-4 border-[#1E6C48] rounded-lg bg-white p-4"
          >
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <span
                ><CircleCheck class="size-6 fill-[#1E6C48] text-white"
              /></span>
              <p class="text-lg font-semibold text-gray-700">Strengths</p>
            </h3>
            <ul class="mt-3 space-y-2">
              <li
                v-for="strength in screenings[screeningIdx].result.strengths"
                :key="strength"
                class="flex items-start gap-2 text-gray-600"
              >
                <span class="text-[#1E6C48] mt-0.5">✓</span>
                {{ strength }}
              </li>
            </ul>
          </div>
          <div
            class="md:col-span-5 border-l-4 border-[#654000] rounded-lg bg-white p-4"
          >
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <span
                ><TriangleAlert class="size-6 fill-[#654000] text-white"
              /></span>
              <p class="text-lg font-semibold text-gray-700">Gaps</p>
            </h3>
            <ul class="mt-3 space-y-2">
              <li
                v-for="weakness in screenings[screeningIdx].result.weaknesses"
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
    </SheetContent>
  </Sheet>
  <div
    class="datatable-wrapper border border-gray-300 rounded-lg bg-[#F2F3FF] text-sm overflow-x-auto"
  >
    <div class="min-w-[680px]">
      <DataTable
        :data="screenings"
        :columns="columns"
        :options="options"
        class="row-border nowrap custom-datatable"
      />
    </div>
  </div>
</template>

<style scoped>
.datatable-wrapper :deep(.dt-search) {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0px 10px !important;
}

.datatable-wrapper :deep(.dt-search input) {
  width: 280px !important;
  padding: 10px 10px !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 8px !important;
  /* background: #ffffff !important; */
  color: #0f172a !important;
  font-size: 14px !important;
  outline: none !important;
}

.datatable-wrapper :deep(table.dataTable thead th),
.datatable-wrapper :deep(table.dataTable tbody td) {
  border-bottom: 1px solid #d8d6e7 !important;
  padding: 16px 16px;
}

.datatable-wrapper :deep(.dt-search input:focus) {
  border-color: #7c3aed !important;
  box-shadow: 0 0 0 1px #7c3aed !;
}

.datatable-wrapper :deep(table.dataTable tbody tr) {
  background: white !important;
}

.datatable-wrapper :deep(table.dataTable tbody td) {
  background: white !important;
}

.datatable-wrapper :deep(.dt-info) {
  padding: 0px 16px !important;
}

.datatable-wrapper :deep(.dt-paging) {
  padding: 0px 16px !important;
}

.datatable-wrapper :deep(.dt-length) {
  padding: 0px 16px !important;
}
</style>
