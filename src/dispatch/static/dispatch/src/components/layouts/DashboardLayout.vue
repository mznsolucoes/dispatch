<template>
  <v-app id="dispatch">
    <!--<loading />-->
    <app-toolbar />
    <app-drawer />
    <notification-snackbars-wrapper />
    <refresh />
    <v-content>
      <!-- Page Header -->
      <page-header />
      <div class="page-wrapper">
        <v-container pa-4 grid-list-lg>
          <v-tabs fixed-tabs v-model="tab" color="primary">
            <v-tab to="incidents">Incidents</v-tab>
            <v-tab to="tasks">Tasks</v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item id="incidents">
              <router-view name="incidents"></router-view>
            </v-tab-item>
            <v-tab-item id="tasks">
              <router-view name="tasks"></router-view>
            </v-tab-item>
          </v-tabs-items>
          <router-view />
        </v-container>
      </div>
    </v-content>
  </v-app>
</template>

<script>
import AppDrawer from "@/components/AppDrawer"
import AppToolbar from "@/components/AppToolbar"
import PageHeader from "@/components/PageHeader"
import Refresh from "@/components/Refresh.vue"
import NotificationSnackbarsWrapper from "@/components/NotificationSnackbarsWrapper.vue"

export default {
  name: "DashboardLayout",

  data() {
    return {
      tab: null
    }
  },
  components: {
    AppDrawer,
    AppToolbar,
    PageHeader,
    Refresh,
    NotificationSnackbarsWrapper
  },

  created() {
    this.$vuetify.theme.light = true
  }
}
</script>

<style scoped>
.page-wrapper {
  min-height: calc(100vh - 64px - 50px - 81px);
}
</style>
