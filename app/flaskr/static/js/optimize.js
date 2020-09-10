$(function () {
    //ポートフォリオ最適化ボタンを押したときに結果を表示するための関数
    $('.optimize-btn').click(function () {
        var read1 = $("#read1").text();
        var read2 = $("#read2").text();
        var read3 = $("#read3").text();
        var read4 = $("#read4").text();
        $.getJSON('/_optimize_result', {
            read1: read1,
            read2: read2,
            read3: read3,
            read4: read4
        }, function (data) {
            if (data.msg.indexOf('エラー') !== 0) {
                $("#optimize_msg").removeClass("changed");
            } else {
                $("#optimize_msg").addClass("changed");
            }

            if ((data.msg === "最適ポートフォリオの出力に成功しました。")
                || (data.msg === "エラー：最適化に失敗しました、別の組み合わせを選択してください。")
            ) {
                $('.plot_img').remove();
                var name = "../static/img/result";
                for (let i = 0; i < data.stock.length; ++i) {
                    name = name + "_" + data.stock[i];
                }
                name = name + ".jpg";
                $('<img class="plot_img" src=' + name + '>')
                    .appendTo('#optimize-plot');
            };
            $("#optimize_msg").text(data.msg);
            $("#keys0").text(data.keys0);
            $("#keys1").text(data.keys1);
            $("#keys2").text(data.keys2);
            $("#keys3").text(data.keys3);
            $("#values0").text(data.values0);
            $("#values1").text(data.values1);
            $("#values2").text(data.values2);
            $("#values3").text(data.values3);
            $("#return").text(data.return);
            $("#risk").text(data.risk);
            $("#sharpratio").text(data.sharpratio);
        });
    });
});

