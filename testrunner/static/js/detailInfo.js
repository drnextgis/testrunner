Vue.component('detailInfo', {
  template: '#detailInfoTemplate',
  props: ["item"],
  data () {
    return {
      visible: false
    }
  },
  watch: {
    item(value){
      if (value != undefined)
        this.show()
      else
        this.hide();
    }
  },
  methods: {
    show(item){
      this.visible = true;
    },
    hide(){
      this.visible = false;
      this.$emit("detailInfo:hidden");
    }
  }
});
