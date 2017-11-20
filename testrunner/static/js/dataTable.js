Vue.component('dataTable', {
  template: '#tableTemplate',
  data () {
    return {
      search: '',
      totalItems: 0,
      items: [],
      activeItem: undefined,
      loading: true,
      pagination: {
        sortBy: "created",
        descending: true
      },
      rowsPerPageItems: [10, 25, 50, {text: "All", value: -1}],
      headers: [
        { text: 'Request ID', value: 'id' },
        { text: 'Requester', align: 'left', value: 'requester' },
        { text: 'Created', align: 'left', value: 'created' },
        { text: 'Test Environment ID', value: 'environment_id' },
        { text: 'Files', align: 'left', value: 'files' }
      ],
      updateInterval: 10000
    }
  },
  watch: {
    pagination: {
      handler () {
        this.getDataFromApi()
      },
      deep: true
    }
  },
  mounted () {
    this.getDataFromApi();
    this.initUpdater();
  },
  methods: {
    getDataFromApi () {
      this.loading = true

      const { sortBy, descending, page, rowsPerPage } = this.pagination
      axios.get(app_url + "api/request/",{
        params:{
          "__sort": descending ? "-" + sortBy : sortBy,
          "__limit": rowsPerPage,
          "__offset": rowsPerPage*(page-1)
        }
      })
        .then(response => {
            this.loading = false;
            this.items = response.data.data
            this.totalItems = response.data.meta.total
        })
        .catch(e => {
            console.error(e)
        });
    },
    initUpdater(){
      let that = this;
      setInterval(function() {
        that.getDataFromApi()
      }, that.updateInterval)
    }
  }   
});
