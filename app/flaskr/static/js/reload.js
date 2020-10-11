$('.btn-square-soft2').click(function () {
        // リセットボタンを押したときに選択情報や表示を初期化する関数
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
    }
);    