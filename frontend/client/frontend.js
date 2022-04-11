import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.esm.browser.js'

Vue.component('loader', {
    template: `
      <div style="display: flex;justify-content: center;align-items: center">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    `
})


new Vue({
    el: '#app',
    data() {
        return {
            root_url: 'http://backend_host_port/contract/api/v1.0/',// use localhost:5000 for dev
            // root_url: 'http://localhost:5000/contract/api/v1.0/',
            loading: false,
            contract: {
                firstName: '',
                lastName: ''
            },
            link: '',
            status_message: ''
        }
    },
    computed: {
        canCreate() {
            const result = this.contract.firstName.trim() && this.contract.lastName.trim()
            console.log('canCreate:', result)
            return result
        },
    },
    methods: {
        async applyContract() {
            this.loading = true
            this.status_message = 'Please wait...'
            const { ...contract } = this.contract
            const contractId = await request(this.root_url + 'apply-contract', 'POST', contract)
            this.link = this.root_url + 'contract-download/' + contractId
            console.log('createContent:', this.link)
            this.status_message = 'Saved'
            this.loading = false
        },
    },
    async mounted() {
        // await this.refreshYears()
    }
})

async function request(url, method = 'GET', data = null) {
    try {
        const headers = {}
        let body
        if (data) {
            headers['Content-Type'] = 'application/json'
            body = JSON.stringify(data)
        }
        const response = await fetch(url, {
            method,
            headers,
            body
        })
        return await response.json()
    } catch (e) {
        console.warn('Error:', e.message)
    }
}
