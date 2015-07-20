<?php
session_start();
if(!isset($_SESSION['user'])) {
    header("Location: login.php");
}
?>
<!DOCTYPE html>
<head>
    <meta charset=utf-8 />
	<title>Handlebars</title>
	<link href="css/style.css" rel="stylesheet" />
	<script src="js/jquery.js"></script>
    <script src="js/handlebars.js"></script>
    <script src="js/ckeditor/ckeditor.js"></script>
    <script id="class-template" type="text/x-handlebars-template">
        <ul>
            {{#each this}}
            <li data-id="{{id}}">
                <div class="innerbox">
                    <img src="{{image}}"/>
                    <div class="titlediv">
                        <span class="title">{{title}}</span>
                        {{#equal hasnote 1}}<span class="note">(有笔记)</span>{{/equal}}
                    </div>
                    <div class="subtitle">{{subtitle}}</div>
                    <div class="subtitle {{#long timespan}} long {{else}} short {{/long}}">时间：{{timespan}}</div>
                </div>
            </li>
            {{/each}}
        </ul>
    </script>
    <script id="pag-template" type="text/x-handlebars-template">
        <ul>
            {{#each this}}
            <li data-id={{index}} {{#if clickable}}class="clickable"{{/if}} {{#if cur}}class="cur"{{/if}}>{{{text}}}</li>
            {{/each}}
        </ul>
    </script>
    <script id="chapter-template" type="text/x-handlebars-template">
        <ul class="titleul">
            {{#each this}}
            <li class="titieli">
                <div class="title">{{addone @index}}、{{title}}</div>
                <ul>
                    {{#each subTitle}}
                    <li class="subtitle">
                        {{addone @../index}}-{{addone @index}}、
                        <a href="http://www.imooc.com/{{titletype}}/{{mid}}" target="_blank">
                        {{title}}</a> 
                        {{#if timespan}}<span class="time">({{timespan}})</span>{{/if}}
                        {{#equal titletype 'code'}}
                            <span class="type">(编程)</span>
                        {{else}}
                            {{#equal titletype 'ceping'}}
                            <span class="type">(练习)</span>
                            {{/equal}}
                        {{/equal}}
                    </li>
                    {{/each}}
                </ul>
            </li>
            {{/each}}
        </ul>
    </script>
    <script id="note-template" type="text/x-handlebars-template">
        <ul class="noteul">
            {{#each this}}
            <li>
                <div class="time">{{formatDate notetime}}</div>
                <div class="content">
                    {{{content}}}
                </div>
            </li>
            {{/each}}
        </ul>
        <div class="btn" id="takeNoteBtn">
            <button>记笔记</button>
        </div>
    </script>
    <script id="nodeedit-template" type="text/x-handlebars-template">
        <div class="textdiv" id="ckeditorContainer">
            <textarea id="noteEditor" name="noteEditor"></textarea>
        </div>
        <div>
            <div class="noteBtn">
                <button id="previewNote">预览</button>
                <button id="submitNote" data-id="{{cid}}">提交</button>
            </div>
        </div>
    </script>
    <script id="notepre-template" type="text/x-handlebars-template">
        <ul class="noteul">
            <li>
                <div class="time">{{formatDate notetime}}</div>
                <div class="content">
                    {{{content}}}
                </div>
            </li>
        </ul>
    </script>
</head>
<body>
    <div class="banner">
        <h1>我的慕课笔记本</h1>
        <h3>你的指尖，有改变世界的力量</h3>
    </div>
    <!-- 课程列表 -->
    <div class="classes" id="classes">
        <!-- 通过Handlebars来渲染html -->
    </div>
    <!-- 翻页 -->
    <div class="pag" id="pag">
        <!-- 通过Handlebars来渲染html -->
    </div>
    <!-- 遮罩 -->
    <div class="overlap"></div>
    <!-- 笔记页 -->
    <div class="notedetail">
        <!-- 章节 -->
        <div class="chapterdiv" id="chapter">
            <!-- 通过Handlebars来渲染html -->
        </div>
        <div class="notemiddle"></div>
        <!-- 笔记 -->
        <div class="notediv" id="note">
            <!-- 通过Handlebars来渲染html -->
        </ul>
        </div>
    </div>
	<script src="js/index.js"></script>
</body>
