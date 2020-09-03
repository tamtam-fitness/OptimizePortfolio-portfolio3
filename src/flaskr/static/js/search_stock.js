$(function () {
    // 銘柄追加ボタンを押したときに表示を初期化する関数
    $('.btn-square-soft').click(function () {
        $('.search_lists').remove();
        $("#search_result1").removeClass("changed");
        $("#memory_msg").text("銘柄を追加");
        $("#memory_msg").addClass("font-bold");
        $("#memory_msg").removeClass("changed");
    });

    // ポップアップ内のsearchボタンを押したときに銘柄が存在するか確認する関数
    $('a#search').bind('click', function () {
        $.getJSON('/_type_in_stock', {
            stock: $('input[name="stock"]').val()
        }, function (data) {
            $("#memory_msg").text("銘柄を追加");
            $("#memory_msg").addClass("font-bold");
            $("#memory_msg").removeClass("changed");
            $('.search_lists').remove();
            $("#search_result1").removeClass("changed");
            // 銘柄が取得できたか
            if (data.search_result1.indexOf('：') !== -1) {
                $('<a class = "search_lists"></a>')
                    .append(data.search_result1)
                    .appendTo('#search_result1');
            } else {
                $('<p class = "search_lists"></p>')
                    .append(data.search_result1)
                    .appendTo('#search_result1');
                $("#search_result1").addClass("changed");
            };

            if (data.search_result2.indexOf('：') !== -1) {
                $('<a class = "search_lists"></a>')
                    .append(data.search_result2)
                    .appendTo('#search_result2');
            };
            if (data.search_result3.indexOf('：') !== -1) {
                $('<a class = "search_lists"></a>')
                    .append(data.search_result3)
                    .appendTo('#search_result3');
            };
            if (data.search_result4.indexOf('：') !== -1) {
                $('<a class = "search_lists"></a>')
                    .append(data.search_result4)
                    .appendTo('#search_result4');
            };
            if (data.search_result5.indexOf('：') !== -1) {
                $('<a class = "search_lists"></a>')
                    .append(data.search_result5)
                    .appendTo('#search_result5');
            };
        });
    });

    //選択した銘柄を押したときに、index.htmlに登録内容を表示する関数
    $('.popup_list li').click(function () {
        var stock_code = $(this).text();
        var read1 = $("#read1").text();
        var read2 = $("#read2").text();
        var read3 = $("#read3").text();
        var read4 = $("#read4").text();
        $.getJSON('/_memorize_stock_code', {
            stock_code: stock_code,
            read1: read1,
            read2: read2,
            read3: read3,
            read4: read4
        }, function (data) {
            $("#memory_msg").text(data.msg);
            $("#memory_msg").removeClass("font-bold");
            if (data.msg.indexOf('成功') !== -1) {
                $("#memory_msg").removeClass("changed");
                if (read1 === "銘柄：未選択") {
                    $("#read1").text(stock_code);
                } else if (read2 === "銘柄：未選択") {
                    $("#read2").text(stock_code);
                } else if (read3 === "銘柄：未選択") {
                    $("#read3").text(stock_code);
                } else if (read4 === "銘柄：未選択") {
                    $("#read4").text(stock_code);
                } else {
                    pass
                };
            } else {
                $("#memory_msg").addClass("changed");
            };
        });
    });
    // リセットボタンを押したときに選択情報や表示を初期化する関数
    $('.btn-square-soft2').click(function () {
        $.getJSON('/_reload_reset_stock', function (data) {
            window.name = data.msg;
            $("#read1").text("銘柄：未選択");
            $("#read2").text("銘柄：未選択");
            $("#read3").text("銘柄：未選択");
            $("#read4").text("銘柄：未選択");
            $("#optimize_msg").text("2名柄以上選択して最適化してください。");
            $("#optimize_msg").removeClass("changed");
            $("#keys0").text("未選択");
            $("#keys1").text("未選択");
            $("#keys2").text("未選択");
            $("#keys3").text("未選択");
            $("#values0").text("ー");
            $("#values1").text("ー");
            $("#values2").text("ー");
            $("#values3").text("ー");
            $("#return").text("ー");
            $("#risk").text("ー");
            $("#sharpratio").text("ー");
            $('.plot_img').remove();
            $('<img class="plot_img" src= "../static/img/no_data_found.png" >')
                .appendTo('#optimize-plot');
            location.reload(True);
        });
    });
    //データを初期化する関数
    $(window).on("unload", function (e) {
        $.getJSON('/_reload_reset_stock', function (data) {
            window.name = data.msg;
        });
    });
});
