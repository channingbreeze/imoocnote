(function($){
    
    // 获取数据的接口
    var GETCLASSES = 'http://imoocnote.calfnote.com/inter/getClasses.php';
    var GETCLASSCHAPTER = 'http://imoocnote.calfnote.com/inter/getClassChapter.php';
    var GETCLASSNOTE = 'http://imoocnote.calfnote.com/inter/getClassNote.php';
    var ADDNOTE = 'http://imoocnote.calfnote.com/inter/addClassNote.php';
    var SEARCHCLASSES = "http://imoocnote.calfnote.com/inter/searchClasses.php";
    
    var g_curPage = 1;
    var g_keyword = '';
    
    // 全局ajax失败处理
    $.ajaxSetup({
        error: function(x, e) {
            alert("调用接口失败");
            return false;
        }
    });
    
    // 点击笔记旁边取消显示笔记
    $(".overlap").on('click', function(e){
        showNote(false);
    });
    
    // 是否显示笔记
    function showNote(show) {
        if(show) {
            $(".overlap").css('display', 'block');
            $(".notedetail").css('display', 'block');
        } else {
            $(".overlap").css('display', 'none');
            $(".notedetail").css('display', 'none');
            searchClasses(g_curPage, g_keyword);
        }
    };
    
    // 封装Handlebars的渲染操作
    function renderTemplate(templateSelector, data, htmlSelector) {
        var template = $(templateSelector).html();
        var classHtml = Handlebars.compile(template)(data);
        $(htmlSelector).html(classHtml);
    };
    
    // 更新课程列表
    function refreshClasses(curPage) {
        $.getJSON(GETCLASSES, 'curPage='+curPage, function(data){
            renderTemplate("#class-template", data.data, "#classes");
            renderTemplate("#pag-template", formatPag(data), "#pag");
            bindClassEvent();
            bindPageEvent();
        });
    };
    
    // 绑定点击课程事件
    function bindClassEvent() {
        $("#classes").find('li').on('click', function(e){
            $this = $(this);
            var cid = $this.data('id');
            $.when($.getJSON(GETCLASSCHAPTER, 'cid='+cid),
                   $.getJSON(GETCLASSNOTE, 'cid='+cid)
            ).done(function(cData, nData) {
                renderTemplate("#chapter-template", cData[0], "#chapter");
                renderTemplate("#note-template", nData[0], "#note");
                bindNoteEvent(cid);
                showNote(true);
            });
        });
    };
    
    // 绑定分页事件
    function bindPageEvent() {
        $("#pag").find('li.clickable').on('click', function(e){
            $this = $(this);
            g_curPage = $this.data('id');
            searchClasses(g_curPage, g_keyword);
        });
    };
    
    // 绑定记笔记事件
    function bindNoteEvent(cid) {
        $("#takeNoteBtn").on('click', function(e){
            renderTemplate("#nodeedit-template", {cid: cid}, "#chapter");
            renderTemplate("#notepre-template", {}, "#note");
            CKEDITOR.replace('noteEditor');
            $("#previewNote").on('click', function(e){
                var d = {};
                d.notetime = new Date().getTime();
                d.content = CKEDITOR.instances.noteEditor.getData();
                renderTemplate("#notepre-template", d, "#note");
            });
            $("#submitNote").on('click', function(e){
                var cid = $(this).data('id');
                var content = CKEDITOR.instances.noteEditor.getData();
                $.post(ADDNOTE, {cid: cid, content: content}, function(data){
                    if(data == "success") {
                        $.when($.getJSON(GETCLASSCHAPTER, 'cid='+cid),
                           $.getJSON(GETCLASSNOTE, 'cid='+cid)
                        ).done(function(cData, nData) {
                            renderTemplate("#chapter-template", cData[0], "#chapter");
                            renderTemplate("#note-template", nData[0], "#note");
                            bindNoteEvent(cid);
                        });
                    } else {
                        window.alert("增加笔记失败");
                    }
                });
                
            });
        });
    };
    
    // 将分页数据格式化为handlerbars需要的数据
    // 与其在Helper中拼接html，不如为handlebars封装数据
    // 对于逻辑复杂的函数，编写可测试代码
    function formatPag(pagData) {
        var arr = [];
        var total = parseInt(pagData.totalCount);
        var cur = parseInt(pagData.curPage);
        // 处理到首页的逻辑
        var toLeft = {};
        toLeft.index = 1;
        toLeft.text = '&laquo;';
        if(cur != 1) {
            toLeft.clickable = true;
        }
        arr.push(toLeft);
        // 处理到上一页的逻辑
        var pre = {};
        pre.index = cur - 1;
        pre.text = '&lsaquo;';
        if(cur != 1) {
            pre.clickable = true;
        }
        arr.push(pre);
        // 处理到cur页前的逻辑
        if(cur <= 5) {
            for(var i=1; i<cur; i++) {
                var pag = {};
                pag.text = i;
                pag.index = i;
                pag.clickable = true;
                arr.push(pag);
            }
        } else {
            // 如果cur>5，那么cur前的页要显示…
            var pag = {};
            pag.text = 1;
            pag.index = 1;
            pag.clickable = true;
            arr.push(pag);
            var pag = {};
            pag.text = '…';
            arr.push(pag);
            for(var i=cur-2; i<cur; i++) {
                var pag = {};
                pag.text = i;
                pag.index = i;
                pag.clickable = true;
                arr.push(pag);
            }
        }
        // 处理到cur页的逻辑
        var pag = {};
        pag.text = cur;
        pag.index = cur;
        pag.cur = true;
        arr.push(pag);
        // 处理到cur页后的逻辑
        if(cur >= total-4) {
            for(var i=cur+1; i<=total; i++) {
                var pag = {};
                pag.text = i;
                pag.index = i;
                pag.clickable = true;
                arr.push(pag);
            }
        } else {
            // 如果cur<total-4，那么cur后的页要显示…
            for(var i=cur+1; i<=cur+2; i++) {
                var pag = {};
                pag.text = i;
                pag.index = i;
                pag.clickable = true;
                arr.push(pag);
            }
            var pag = {};
            pag.text = '…';
            arr.push(pag);
            var pag = {};
            pag.text = total;
            pag.index = total;
            pag.clickable = true;
            arr.push(pag);
        }
        // 处理到下一页的逻辑
        var next = {};
        next.index = cur + 1;
        next.text = '&rsaquo;';
        if(cur != total) {
            next.clickable = true;
        }
        arr.push(next);
        // 处理到尾页的逻辑
        var toRight = {};
        toRight.index = total;
        toRight.text = '&raquo;';
        if(cur != total) {
            toRight.clickable = true;
        }
        arr.push(toRight);
        return arr;
    };
    
    Handlebars.registerHelper("formatDate", function(value) {
        if(!value) {
            return "";
        }
        var d = new Date(value);
        var year = d.getFullYear();
        var month = d.getMonth() + 1;
        var date = d.getDate();
        var hour = d.getHours();
        var minute = d.getMinutes();
        var second = d.getSeconds();
        var str = year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
        return str;
    });
    
    Handlebars.registerHelper("equal", function(v1, v2, options) {
        if(v1 == v2) {
            return options.fn(this);
        } else {
            return options.inverse(this);
        }
    });
    
    Handlebars.registerHelper("long", function(v, options) {
        if(v.indexOf('小时') != -1) {
            return options.fn(this);
        } else {
            return options.inverse(this);
        }
    });
    
    Handlebars.registerHelper("addone", function(v) {
        return v+1;
    });
    
    refreshClasses(1);
    
    // 搜索课程列表
    function searchClasses(curPage, keyword) {
        $.getJSON(SEARCHCLASSES, 'curPage='+curPage + '&keyword=' + keyword, function(data){
            g_curPage = curPage;
            renderTemplate("#class-template", data.data, "#classes");
            renderTemplate("#pag-template", formatPag(data), "#pag");
            bindClassEvent();
            bindPageEvent();
        });
    };
    
    var t;
    $("#searchInput").on('keydown', function() {
        $this = $(this);
        if(t) {
            clearTimeout(t);
            t = null;
        }
        t = setTimeout(function() {
            g_keyword = $this.val();
            searchClasses(1, g_keyword);
            clearTimeout(t);
            t = null;
        } ,500);
    });
    
})(jQuery);