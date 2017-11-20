new Vue({ 
  el: '#app',
  data () {
    return {
      snackbar: {
          visibility: false,
          color: undefined,
          text: undefined,
          timeout: 5000
      }
    }
  },
  methods: {
    showSnackbar(color, text){
        this.snackbar.visibility = true
        this.snackbar.color = color
        this.snackbar.text = text
    },
    onFormSubmitted(){
        this.$refs.dataTable.getDataFromApi()
        this.showSnackbar('success', 'Request Was Submitted Successfully')
    },
    onFormFailed(message){
        this.showSnackbar('error', message)
    }
  }
});
