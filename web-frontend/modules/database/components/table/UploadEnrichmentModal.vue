<template>
  <Modal>
    <h2 class="box__title">Upload servers to enrich</h2>
    <Error :error="error"></Error>
    <TableForm ref="tableForm" @submitted="submitted">
      <form @submit.prevent="submit">
        <div class="control">
          <label class="control__label">
            <i class="fas fa-font"></i>
            Exploit
          </label>
          <div class="control__elements">
            <input
              ref="exploit"
              v-model="values.exploit"
              type="text"
              class="input input--large"
            />
          </div>
        </div>
      </form>
      <component :is="importerComponent" />
      <div class="actions">
        <div class="align-right">
          <button
            class="button button--large"
            :class="{ 'button--loading': loading }"
            :disabled="loading"
          >
            Upload
          </button>
        </div>
      </div>
    </TableForm>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import TableCSVImporter from '@baserow/modules/database/components/table/TableCSVImporter'
import TableForm from './TableForm'

export default {
  name: 'UploadEnrichmentModal',
  components: { TableForm },
  mixins: [modal, error],
  props: {
    application: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
      values: {
        name: '',
      },
      importer: '',
    }
  },
  computed: {
    importerTypes() {
      return this.$registry.getAll('importer')
    },
    importerComponent() {
      return TableCSVImporter
    },
  },
  methods: {
    hide(...args) {
      modal.methods.hide.call(this, ...args)
      this.importer = ''
    },
    /**
     * When the form is submitted we try to extract the initial data and first row
     * header setting from the values. An importer could have added those, but they
     * need to be removed from the values.
     */
    async submitted(values) {
      this.loading = true
      this.hideError()

      let firstRowHeader = false
      let data = null

      if (Object.prototype.hasOwnProperty.call(values, 'firstRowHeader')) {
        firstRowHeader = values.firstRowHeader
        delete values.firstRowHeader
      }

      if (Object.prototype.hasOwnProperty.call(values, 'data')) {
        data = JSON.parse(values.data)
        delete values.data
      }

      try {
        const table = await this.$store.dispatch('table/create', {
          database: this.application,
          values,
          initialData: data,
          firstRowHeader,
        })
        this.loading = false
        this.hide()

        // Redirect to the newly created table.
        this.$nuxt.$router.push({
          name: 'database-table',
          params: {
            databaseId: this.application.id,
            tableId: table.id,
          },
        })
      } catch (error) {
        this.loading = false
        this.handleError(error, 'application')
      }
    },
  },
}
</script>
