/**
 * Created by ding on 17/5/4.
 */
Vue.config.devtools = true;

    var imgthumb= {
        props:['each_file','index'],
        template:`
            <section class="up-section loading fl">
                <span class="up-span"></span>
                <img class='close-upimg' src="../../static/images/baseform/a7.png" @click="delconfirm">
                <img class='up-img up-opcity' v-bind:src="getfileurl">
           </section>
        `,
        computed:{
            getfileurl:function () {
                return window.URL.createObjectURL(this.each_file)
            }
        },
        methods:{
            delconfirm:function () {
                app.file_L.splice(this.index,1);
                var num = app.file_L.length;
                if(num < 9){
			        $("#z_file").show();
		        }
            }
        }
    }

  var imgbox = {
            template:`
            <div class="img-section">
                                <!--<p class="up-p"><span class="up-span">最多可以上传9张图片</span></p>-->
                <div class="z_photo upimg-div clear" >
                    <imgthumb v-for="each_file in file_L"></imgthumb>
                    <section class="z_file fl" id="z_file">
                            <img src="static/images/addpic.png" class="add-img">
                         <input type="file" name="file" id="testup" class="file" value="" accept="image/jpg,image/jpeg,image/png,image/bmp" multiple /> 
                    </section>
                </div>
    
             </div>
            `
        }


    var loader = {
        template:`
        <div class="loader loader-mask">

            <div class="loader-inner   loader-content">
                <div class="ball-pulse">
                 <div></div>
        
                  <div></div>
        
                  <div></div>
                </div>
            <label id="loader-upspan">文件传输中...</label>
    
            </div>

        </div>
        `
    }

    


        var app = new Vue({
            el:'#mainwin',
            data:{
                name:null,
                sex:null,
                born:null,
                city:null,
                tel:null,
                email:null,
                qq:null,
                wx:null,
                school:null,
                major:null,
                graduate:null,
                 seen1:true,
                 seen2:false,
                 seen3:false,
                 seen4:false,
                category:[],
                 category1:[],
                 category2:[],
                 category3:[],
                 worktime:[],
                identity:null,
                 project_text:null,
                blog_url:null,
                file_L : [],
                img_url:[],
                loaderseen:false,
                applystatus:null,
                isapplyed:true
            },
            methods:{
                showform1:function(){
                    this.seen1=true;
                    this.seen2=false;
                    this.seen3=false;
                    window.scrollTo(0,0);

                },
                valid_form1:function () {
                    var that = this;
                      var validator = $("#form").validate({
                        submitHandler:function (form) {
                            that.showform2();
                        },

                 //        errorPlacement: function(error, element) {
			//Append error within linked label
               // alert("t");
                      //},
                            rules: {
                                name: "required",

                                sex: "required",
                                born: {
                                     required:true,
                                    number:true
                                },
                                city: "required",
                                tel: {
                                    required:true,
                                    maxlength:11,
                                    minlength:11
                                },
                                email: {
                                    required:true,
                                    email:true
                                },
                                school: "required",
                                major: "required",
                                graduate: {
                                     required:true,
                                    number:true
                                },
                            },
                     });
                },
                showform2:function () {
                    this.seen2=true;
                     this.seen1=false;
                     this.seen3=false;
                    window.scrollTo(0,0);
                },

                 showform3:function(){
                    this.seen3=true;
                    this.seen2=false;
                    this.seen1=false;
                     window.scrollTo(0,0);
                },
                 showform4:function(){
                    this.seen4=true;
                    this.seen2=false;
                    this.seen1=false;
                     this.seen3=false;
                     window.scrollTo(0,0);
                },
                appendfile:function (file) {
                    this.file_L.push(file);
                },
                submitapply:function () {
                    //get checked
                     var cat = $("input[name='category']:checked");
                     for(var i=0; i<cat.length; i++){
                         this.category.push(cat[i].value);
                     }

                    var wor = $("input[name='worktime']:checked");
                     for(var i=0; i<wor.length; i++){
                         this.worktime.push(wor[i].value);
                     }

                    var iden = $("input[name='identity']:checked");
                    if(iden[0]!=null){
                        this.identity = iden[0].value;
                    }

                    //upload file
                    if(this.file_L.length!=0){
                        this.loaderseen= true;
                        uploader.addFile(this.file_L);
                    }
                    else{
                        alert("请上传文件");
                    }
                    //这里要阻塞 等待添加完成

                    //get work_url
                    
                    // this.seen1 = this.seen2 = this.seen3 = false;
                    // this.seen4 = true;
                    // var that = this;
                    // $.ajax({
                    //         url:'api/v1.0/apply/form',
                    //         type:'POST',
                    //         async: false,
                    //         data:{
                    //             name: that.name,
                    //             sex: that.sex,
                    //             born: that.born,
                    //             tel: that.tel,
                    //             email: that.email,
                    //             qq: that.qq,
                    //             wx: that.wx,
                    //             school: that.school,
                    //             major: that.major,
                    //             graduate: that.graduate,
                    //
                    //              category:JSON.stringify(that.category),
                    //
                    //              worktime:JSON.stringify(that.worktime),
                    //             identity:that.identity,
                    //              project_text:that.project_text,
                    //             blog_url:  that.blog_url,
                    //             img_url:  JSON.stringify(that.img_url),
                    //         },
                    //        timeout:5000,    //超时时间
                    //         dataType:'json',
                    //         success:function(result) {
                    //             showform4();
                    //         }
                    //     });
                    // window.scrollTo(0,0);
                }

            },
            components:{
                'imgthumb':imgthumb,
                'loader':loader
            },
            created:function () {
                var that = this;
               $.ajax({
                     url:'api/v1.0/apply/status',
                    type:'GET',
                    async: false,
                   timeout:5000,    //超时时间
                    dataType:'json',
                    success:function(result) {
                        that.applystatus = parseInt(result['applystatus'])
                    },
                    error:function (data) {
                        that.applystatus = 0;
                    }
                });
                if(that.applystatus==1){  //已提交审核中
                    that.isapplyed=false
                    that.seen4 = true
                }
            },
            mounted:function () {
                var that = this;
                $('input').iCheck({
                                checkboxClass: 'icheckbox_square-green',
                                 radioClass: 'iradio_square-green',
                                increaseArea: '20%' // optional
                      });

                // $("input[name='category']").on('ifChecked', function(event){
                //         that.category.push(this.value);
                //     });
                // $("input[name='category']").on('ifUnchecked', function(event){
                //
                //     });

                registerup();
            }

        })



