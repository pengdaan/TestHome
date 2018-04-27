/*!
 * Remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */

function buildTable($el, cells, rows) {
  var i, j, row,
    columns = [],
    data = [];

  for (i = 0; i < cells; i++) {
    columns.push({
      field: '字段' + i,
      title: '单元' + i
    });
  }
  for (i = 0; i < rows; i++) {
    row = {};
    for (j = 0; j < cells; j++) {
      row['字段' + j] = 'Row-' + i + '-' + j;
    }
    data.push(row);
  }
  $el.bootstrapTable('destroy').bootstrapTable({
    columns: columns,
    data: data,
    iconSize: 'outline',
    icons: {
      columns: 'glyphicon-list'
    }
  });
}

(function(document, window, $) {

  buildTable($('#exampleTableLargeColumns'), 50, 50);
  (function() {
    $('#exampleTableEvents').bootstrapTable({
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        search: true,
        pagination: true, //是否显示分页（*）
        showRefresh: true, //是否显示刷新按钮
        showToggle: true,  //是否显示详细视图和列表视图的切换按钮
        showColumns: true, //是否显示所有的列
        iconSize: 'outline',
        toolbar: '#exampleTableEventsToolbar',
        icons: {
          refresh: 'glyphicon-repeat',
          toggle: 'glyphicon-list-alt',
          columns: 'glyphicon-list'
        }
    });
    $('#exampleTableEvents').on('all.bs.table', function(e, name, args) {
        console.log('Event:', name, ', data:', args);
      })
  })();
})(document, window, jQuery);
