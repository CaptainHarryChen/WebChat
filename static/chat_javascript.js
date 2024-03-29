var selfName = "";
var active_name = "";
var friends_msgid = {};

function GetCurTime() {
    var myDate = new Date;
    var year = myDate.getFullYear();
    var mon = myDate.getMonth() + 1;
    var date = myDate.getDate();
    var h = myDate.getHours();
    var m = myDate.getMinutes();
    var s = myDate.getSeconds();
    return PrefixInteger(year, 4) + "/" + PrefixInteger(mon, 2) + "/" + PrefixInteger(date, 2) + " " + PrefixInteger(h, 2) + ":" + PrefixInteger(m, 2) + ":" + PrefixInteger(s, 2);
}

function PrefixInteger(num, length) {
    return ("0000000000000000" + num).substr(-length);
}

function GetCurTime(type = 1) {
    var myDate = new Date;
    var year = PrefixInteger(myDate.getFullYear(), 4);
    var mon = PrefixInteger(myDate.getMonth() + 1, 2);
    var date = PrefixInteger(myDate.getDate(), 2);
    var h = PrefixInteger(myDate.getHours(), 2);
    var m = PrefixInteger(myDate.getMinutes(), 2);
    var s = PrefixInteger(myDate.getSeconds(), 2);
    if (type == 1)
        return year + "/" + mon + "/" + date + " " + h + ":" + m + ":" + s;
    else if (type == 2)
        return year + mon + date + h + m + s;
    else if (type == 3)
        return mon + "/" + date + " " + h + ":" + m;
}

function ChangeTimeFormat(time) {
    var year = time.slice(0, 4);
    var mon = time.slice(4, 6);
    var date = time.slice(6, 8);
    var h = time.slice(8, 10);
    var m = time.slice(10, 12);
    var s = time.slice(12, 14);
    return year + "/" + mon + "/" + date + " " + h + ":" + m + ":" + s;
}

function AddFriendBox(name, time = "", content = "", mode = "append") {
    if (time != "")
        time = time.slice(5, 6) + "-" + time.slice(6, 8) + " " + time.slice(8, 10) + ":" + time.slice(10, 12);
    var str = '<div id="friend_' + name + '" class="friend_box row_container" name="' + name + '"><img src="./static/avatar.jfif" class="avatar"><div class="col_container card_box"><div class="row_container card_title"><div class="card_name">' + name + '</div><div class="card_time">' + time + '</div></div><div class="card_content">' + content + '</div></div></div>';
    if (mode = "append")
        $("#friends").append(str);
    else if (mode = "prepend")
        $("#friends").prepend(str);
    $("#friend_" + name).click(OnFriendBoxClick);
}

$(document).ready(function () {
    $("#add_friend").click(AddFriend);
    $("#send_button").click(OnSendMsg);
    $(".friend_box").click(OnFriendBoxClick);
    $("#create_group").click(OnCreateGroup);
    $("#logout_button").click(OnLogout);

    $.post("/GetSelfName", {}, function (ret) {
        $("#self").html(ret);
        selfName = ret;
    });
    $.post("/GetFriends", {}, function (ret) {
        var data = $.parseJSON(ret);
        for (i in data) {
            AddFriendBox(data[i]["name"], data[i]["time"], data[i]["content"]);
            friends_msgid[data[i]["name"]] = parseInt(data[i]["id"]);
        }
        setInterval("CheckMsgUpdate()", 3000);
        setInterval("UpdateFriendList()", 20000);
    });
});

function UpdateFriendList() {
    $.post("/UpdateFriendList", {}, function (ret) {
        var data = $.parseJSON(ret);
        for (i in data) {
            AddFriendBox(data[i]["name"], data[i]["time"], data[i]["content"], mode = "prepend");
            friends_msgid[data[i]["name"]] = parseInt(data[i]["id"]);
        }
    });
}

function AddFriend() {
    if (selfName == "")
        return;
    var friend_name = prompt("输入好友名称", "");
    $.post("/AddFriend", { "user1": selfName, "user2": friend_name }, function (ret) {
        if (ret == "not-exist")
            alert("该用户不存在");
        else if (ret == "exist")
            alert("该好友已存在");
        else {
            alert("添加成功");
            friends_msgid[friend_name] = 0;
            AddFriendBox(friend_name, "prepend");
        }
    });
}

function SetMsgLog(name) {
    $("#friend_name").html(name);
    $("#msg_log").html('<div id="msg_loading" class="center"><div class="center">加载中……</div></div>');
    var typ = selfName;
    if (active_name.slice(0, 5) == "Group")
        typ = "Group";
    $.post("/GetMsgLog", { "class": typ, "name": name }, function (ret) {
        var logs = $.parseJSON(ret);
        $("#msg_log").html("");
        ShowMsgLog(logs);
    });
}

function OnFriendBoxClick() {
    $(".friend_box").removeClass("active");
    $(this).addClass("active");
    active_name = $(this).attr("name");
    SetMsgLog($(this).attr("name"));
    $("#chat_input .mask").css("display", "none");
}

function OnCreateGroup() {
    $("#create_group_popup .checkboxs").html("");
    for (key in friends_msgid)
        if (key.slice(0, 5) != 'Group' && key != selfName)
            $("#create_group_popup .checkboxs").append('<input type="checkbox" value="' + key + '">' + key + '<br>');
    $("#create_group_popup").css("display", "block");
}

function OnConfirmCreateGroup() {
    var chosen = [];
    $("#create_group_popup input:checked").each(function () {
        chosen.push($(this).val());
    });
    $.post("/CreateGroup", { "users": chosen.toString() }, function (ret) {
        friends_msgid[ret] = 0;
        AddFriendBox(ret, "prepend");
    });
    $("#create_group_popup").css("display", "none");
}

function OnCloseCreateGourpPopup() {
    $("#create_group_popup").css("display", "none");
}

function ShowMsgLog(logs) {
    for (i in logs) {
        var name = logs[i][1];
        var time = logs[i][2];
        var content = logs[i][3];
        time = PrefixInteger(time.slice(0, 4), 4) + "/" + PrefixInteger(time.slice(4, 6), 2) + "/" + PrefixInteger(time.slice(6, 8), 2) + " " + PrefixInteger(time.slice(8, 10), 2) + ":" + PrefixInteger(time.slice(10, 12), 2) + ":" + PrefixInteger(time.slice(12, 14), 2);
        content = content.replace("\r\n", "<br>");
        content = content.replace("\n", "<br>");
        $("#msg_log").append('<div class="onemsg"><header class="onemsg-header">' + name + ' ' + time + '</header><div class="onemsg-content">' + content + '</div></div>');
    }
    $("#div_msg_log").scrollTop($("#div_msg_log").prop("scrollHeight"));
}

function OnSendMsg() {
    var name = selfName;
    var time = GetCurTime(1);
    var content = $("#input_box").val();
    content = content.replace("\r\n", "<br>");
    content = content.replace("\n", "<br>");
    $("#input_box").val("");
    $("#msg_log").append('<div class="onemsg"><header class="onemsg-header">' + name + ' ' + time + '</header><div class="onemsg-content">' + content + '</div></div>');
    $("#div_msg_log").scrollTop($("#div_msg_log").prop("scrollHeight"));
    $(".friend_box.active .card_time").html(GetCurTime(3));
    $(".friend_box.active .card_content").html(content.slice(0, 20));
    friends_msgid[active_name]++;
    var typ = selfName;
    if (active_name.slice(0, 5) == "Group")
        typ = "Group";
    $.post("/recieveMsg", { "class": typ, "name": active_name, "time": GetCurTime(2), "msg": content });
}

function CheckMsgUpdate() {
    $.post("/CheckMsgUpdate", {}, function (ret) {
        var data = $.parseJSON(ret);
        for (i in data) {
            var ele = "#friend_" + data[i]["name"]
            var time = data[i]["time"];
            if (time != "")
                time = time.slice(5, 6) + "-" + time.slice(6, 8) + " " + time.slice(8, 10) + ":" + time.slice(10, 12);
            $(ele + " .card_time").html(time);
            $(ele + " .card_content").html(data[i]["content"])
            if (active_name == data[i]["name"]) {
                //alert(123);
                var typ = selfName;
                if (active_name.slice(0, 5) == "Group")
                    typ = "Group";
                $.post("/GetNewMsg", { "class": typ, "name": active_name, "id": friends_msgid[active_name] }, function (ret) {
                    var logs = $.parseJSON(ret);
                    ShowMsgLog(logs);
                });
            }
            friends_msgid[data[i]["name"]] = parseInt(data[i]["id"]);
        }
    });
}

function OnLogout() {
    window.location.href = "/logout";
}