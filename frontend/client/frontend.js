import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.esm.browser.js'

new Vue({
    el: '#app',
    data() {
        return {
            root_url: 'http://backend_host_port/contract/api/v1.0/',
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
            this.status_message = 'Please wait...'
            const { ...contract } = this.contract
            const contractId = await request(this.root_url + 'apply-contract', 'POST', contract)
            this.link = this.root_url + 'contract-download/' + contractId
            console.log('createContent:', this.link)
            this.status_message = 'Saved'
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
