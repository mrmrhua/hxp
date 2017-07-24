var uploader

function registerup() {
// 上传文件相关
    uploader = Qiniu.uploader({
        runtimes: 'html5,flash,html4',
        browse_button: 'tt',
        // container: 'mainwin',
        // drop_element: 'container',
        flash_swf_url: 'bower_components/plupload/js/Moxie.swf',
        // dragdrop: true,
        chunk_size: '4mb',

        uptoken_url: 'http://127.0.0.1:5000/api/v1.0/apply/uptoken',
        // uptoken:"um6IEH7mtwnwkGpjImD08JdxlvViuELhI4mFfoeL:zPVaMyRvtEgsfbKKuIPpMobH6nc=:eyJzY29wZSI6ImphdmFkZW1vIiwiZGVhZGxpbmUiOjIzNjY1NjI3MjZ9Cg==",
        multi_selection: !(mOxie.Env.OS.toLowerCase() === "ios"),


        filters: {
            max_file_size: '100mb',
            prevent_duplicates: false,
            //Specify what files to browse for
            mime_types: [
                // {title : "mp4 files", extensions : "mkv"}
                // {title : "flv files", extensions : "flv,jpg"}
                // {title : "Video files", extensions : "flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4"}
                // {title : "Video files", extensions : "avi,mp4,wmv,mpg,mov,flv,mkv,mpeg"}
                {title: "Image files", extensions: "jpg,gif,png,jpeg"}
                // {title : "Zip files", extensions : "zip"}
            ]
        },
        // uptoken_func: function(){
        //     var ajax = new XMLHttpRequest();
        //     ajax.open('GET', $('#uptoken_url').val(), false);
        //     ajax.setRequestHeader("If-Modified-Since", "0");
        //     ajax.send();
        //     if (ajax.status === 200) {
        //         var res = JSON.parse(ajax.responseText);
        //         console.log('custom uptoken_func:' + res.uptoken);
        //         return res.uptoken;
        //     } else {
        //         console.log('custom uptoken_func err');
        //         return '';
        //     }
        // },
        domain: 'opf62mkln.bkt.clouddn.com',
        get_new_uptoken: false,
        // downtoken_url: '/downtoken',
        unique_names: true,
        // save_key: true,
        auto_start: true,
        log_level: 5,
        init: {
            'FilesAdded': function(up, files) {
                // $('table').show();
                // $('#success').hide();
                // plupload.each(files, function(file) {
                //     var progress = new FileProgress(file, 'fsUploadProgress');
                //     progress.setStatus("等待...");
                //     progress.bindUploadCancel(up);
                // });
                // alert("add");

            },
            'BeforeUpload': function(up, file) {
                // var progress = new FileProgress(file, 'fsUploadProgress');
                // var chunk_size = plupload.parseSize(this.getOption('chunk_size'));
                // if (up.runtime === 'html5' && chunk_size) {
                //     progress.setChunkProgess(chunk_size);
                // }

            },
            'UploadProgress': function(up, file) {
                // var progress = new FileProgress(file, 'fsUploadProgress');
                // var chunk_size = plupload.parseSize(this.getOption('chunk_size'));
                // progress.setProgress(file.percent + "%", file.speed, chunk_size);
            },
            'UploadComplete': function() {
                 $.ajax({
                            url:'api/v1.0/apply/form',
                            type:'POST',
                            async: false,
                            data:{
                                name: $.trim(app.name),
                                sex:  $.trim(app.sex),
                                born:  $.trim(app.born),
                                tel:  $.trim(app.tel),
                                email:  $.trim(app.email),
                                qq:  $.trim(app.qq),
                                wx:  $.trim(app.wx),
                                school:  $.trim(app.school),
                                major:  $.trim(app.major),
                                graduate:  $.trim(app.graduate),

                                 category:JSON.stringify(app.category),

                                 worktime:JSON.stringify(app.worktime),
                                identity:app.identity,
                                 project_text: $.trim(app.project_text),
                                blog_url:   $.trim(app.blog_url),
                                img_url:  JSON.stringify(app.img_url),
                            },
                           timeout:5000,    //超时时间
                            dataType:'json',
                            success:function(result) {
                                app.loaderseen = false;
                                app.showform4();
                            },
                            error:function (data) {
                                app.loaderseen = false;
                                alert('网络拥挤,请稍后再试')
                            }
                        });

            },
            'FileUploaded': function(up, file, info) {
                //http://developer.qiniu.com/docs/v6/api/overview/up/response/simple-response.html
           //     {
             //   "hash": "Fh8xVqod2MQ1mocfI4S4KpRL6D98",
              //      "key": "gogopher.jpg",
              //      }

                // var progress = new FileProgress(file, 'fsUploadProgress');
                // progress.setComplete(up, info);
                // 成功返回
                if(info['status']=='200') {
                    var tmp = JSON.parse(info['response']);
                    app.img_url.push('http://opf62mkln.bkt.clouddn.com/o_1bfm2neq33o01c9qustv6muj87.png'+tmp.key);

                //     var file_url = 'http://oogj672bg.bkt.clouddn.com/' + tmp.key;
                //     //发送请求
                //     $.ajax({
                //         url: '/api/v1.0/project/add_history_work',
                //         type: 'POST',
                //         async: false,
                //         data: {
                //             work_url: file_url,
                //             pro_id: pro_id,
                //             now_is: now_order
                //
                //         },
                //         timeout: 5000,    //超时时间
                //         dataType: 'json',
                //         success: function (result) {
                //            alert("插入成功");
                //             window.location.reload();
                //         }
                //
                //     });
                }
                // alert("ok");

             },
            'Error': function(up, err, errTip) {
                // $('table').show();
                // var progress = new FileProgress(err.file, 'fsUploadProgress');
                // progress.setError();
                // progress.setStatus(errTip);
                    alert('上传错误:'+errTip);
            }
                // ,
                // 'Key': function(up, file) {
                //     var key = "";
                //     // do something with key
                //     return key
                // }
        }
    });
}

