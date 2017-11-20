Vue.component('recordForm', {
  template: '#recordFormTemplate',
  data () {
    return {
      visible: false,
      requester: undefined,
      environmentId: undefined,
      files: [],
      environmentIdItems: [],
      testItems: []
    }
  },
  mounted(){
    this.getSelectsItems();
  },
  methods: {
    showForm(){
      this.visible = true;
    },
    hideForm(){
      this.visible = false;
    },
    getSelectsItems(){
      // get environment ids
      axios.get(app_url + "api/environment/")
        .then(response => {
            this.environmentIdItems = response.data.data.map((item) => { return item.id })
        })
        .catch(e => {
            console.error(e)
        });

      // get test items
      axios.get(app_url + "api/test/")
        .then(response => {
            this.testItems = response.data;
        })
        .catch(e => {
            console.error(e)
        });
    }, 
    submitForm(){
      axios.post(app_url + "api/request/", {
          requester: this.requester,
          environment_id: this.environmentId,
          files: JSON.stringify(this.files, null, 2)
      })
        .then(response => {
            this.hideForm()
            this.$emit("form:submitted")
        })
        .catch(e => {
            this.$emit("form:failed", e.response.data.description)
        });
    }
  }
});
