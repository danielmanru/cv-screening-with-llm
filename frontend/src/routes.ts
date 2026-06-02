import DefaultLayout from "./components/layouts/DefaultLayout.vue";
import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "@/pages/Dashboard.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: DefaultLayout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: Dashboard,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
