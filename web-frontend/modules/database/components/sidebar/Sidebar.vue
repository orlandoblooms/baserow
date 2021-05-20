<template>
  <SidebarApplication
    :application="application"
    :group="group"
    @selected="selected"
  >
    <template v-if="application._.selected" #body>
      <ul class="tree__subs">
        <SidebarItem
          v-for="table in application.tables"
          :key="table.id"
          :database="application"
          :table="table"
        ></SidebarItem>
      </ul>
      <a
        v-if="group.permissions === 'ADMIN'"
        class="tree__sub-add"
        @click="$refs.createTableModal.show()"
      >
        <i class="fas fa-plus"></i>
        Create table
      </a>
      <a
        class="tree__sub-add"
        @click="$refs.createUploadEnrichmentModal.show()"
      >
        <i class="fas fa-plus"></i>
        Upload data for enrichment
      </a>
      <CreateTableModal
        ref="createTableModal"
        :application="application"
      ></CreateTableModal>
      <UploadEnrichmentModal
        ref="createUploadEnrichmentModal"
        :application="application"
      ></UploadEnrichmentModal>
    </template>
  </SidebarApplication>
</template>

<script>
import { notifyIf } from '@baserow/modules/core/utils/error'
import SidebarItem from '@baserow/modules/database/components/sidebar/SidebarItem'
import CreateTableModal from '@baserow/modules/database/components/table/CreateTableModal'
import UploadEnrichmentModal from '@baserow/modules/database/components/table/UploadEnrichmentModal'
import SidebarApplication from '@baserow/modules/core/components/sidebar/SidebarApplication'

export default {
  name: 'Sidebar',
  components: {
    SidebarApplication,
    SidebarItem,
    CreateTableModal,
    UploadEnrichmentModal,
  },
  props: {
    application: {
      type: Object,
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },
  },
  methods: {
    async selected(application) {
      try {
        await this.$store.dispatch('application/select', application)
      } catch (error) {
        notifyIf(error, 'group')
      }
    },
  },
}
</script>
