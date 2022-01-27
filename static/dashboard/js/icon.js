var myMap;

function range(start, end) {
  var ans = [];
  for (let i = start; i <= end; i++) {
    ans.push(i);
  }
  return ans;
}

ymaps.ready(function () {
  myMap = new ymaps.Map(
    "map",
    {
      center: [41.31707474824766, 69.23678747256474],
      zoom: 12,
    },
    {
      searchControlProvider: "yandex#search",
    }
  );

  // Создаём макет содержимого.
  MyIconContentLayout = ymaps.templateLayoutFactory.createClass(
    '<div style="color: #FFFFFF; font-weight: bold;">$[properties.iconContent]</div>'
  );

  for (let i = 0; i < cords.length; i++) {
    const cord = cords[i][0];
    myMap.geoObjects.add(
      new ymaps.Placemark(
        cord,
        {
          // hintContent: 'Собственный значок метsdfsdfsdfки с контентом',
          // balloonContent: 'А эта — новогодняя',
          // iconContent: '12'
        },
        {
          iconLayout: "default#imageWithContent",
          iconImageHref: "/static/dashboard/img/loc.png",
          iconImageSize: [48, 48],
          iconImageOffset: [-24, -24],
          iconContentOffset: [15, 15],
          iconContentLayout: MyIconContentLayout,
        }
      )
    );
  }
  for (let i = 0; i < adds.length; i++) {
    const addd = adds[i][0];
    myMap.geoObjects.add(
      new ymaps.Placemark(
        addd,
        {
          hintContent: adds[i][1],
          balloonContent: adds[i][1],
          // iconContent: '12'
        },
        {
          iconLayout: "default#imageWithContent",
          iconImageHref: "/static/dashboard/img/fil.png",
          iconImageSize: [48, 48],
          iconImageOffset: [-24, -24],
          iconContentOffset: [15, 15],
          iconContentLayout: MyIconContentLayout,
        }
      )
    );
  }
  const x = (start, end) => {
    // var [year, month, day] = start.format("YYYY-MM-DD").split("-").map((obj) =>{
    //   return parseInt(obj, 10);
    // });
    // var [end_year, end_month, end_day] = end.format("YYYY-MM-DD").split("-").map((obj) =>{
    //   return parseInt(obj, 10);
    // });
    myMap.geoObjects.removeAll();

    for (let i = 0; i < adds.length; i++) {
      const addd = adds[i][0];
      myMap.geoObjects.add(
        new ymaps.Placemark(
          addd,
          {
            hintContent: adds[i][1],
            balloonContent: adds[i][1],
          },
          {
            iconLayout: "default#imageWithContent",
            iconImageHref: "/static/dashboard/img/fil.png",
            iconImageSize: [48, 48],
            iconImageOffset: [-24, -24],
            iconContentOffset: [15, 15],
            iconContentLayout: MyIconContentLayout,
          }
        )
      );
    }

    var start_time = start._d.getTime();
    var end_time = end._d.getTime();
    for (const cordinate of cords) {
      if ( new Date(cordinate[1]).getTime() >= start_time && new Date(cordinate[1]).getTime() <= end_time ) {
        myMap.geoObjects.add(
          new ymaps.Placemark(
            cordinate[0],
            {},
            {
              iconLayout: "default#imageWithContent",
              iconImageHref: "/static/dashboard/img/loc.png",
              iconImageSize: [48, 48],
              iconImageOffset: [-24, -24],
              iconContentOffset: [15, 15],
              iconContentLayout: MyIconContentLayout,
            }
          )
        );
      }
    }

    // for (const cordinate of cords) {
    //   var [c_year, c_month, c_day] = cordinate[1];
    //   console.log([c_year, c_month, c_day],"c");
    //   console.log([end_year, end_month, end_day],"e");
    //   console.log([year, month, day]);
    //

    // }
  };

  $("#daterange-btn").daterangepicker(
    {
      ranges: {
        Сегодня: [moment(), moment()],
        Вчера: [moment().subtract(1, "days"), moment().subtract(1, "days")],
        "Последние 7 дней": [moment().subtract(6, "days"), moment()],
        "Последние 30 дней": [moment().subtract(29, "days"), moment()],
        "Этот месяц": [moment().startOf("month"), moment().endOf("month")],
        "Прошлый месяц": [
          moment().subtract(1, "month").startOf("month"),
          moment().subtract(1, "month").endOf("month"),
        ],
      },
      startDate: moment().subtract(29, "days"),
      endDate: moment(),
    },

    x
  );

  $("#timepicker").datetimepicker({
    format: "LT",
  });
});
