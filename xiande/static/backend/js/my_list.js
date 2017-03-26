  jQuery(document).ready(function() {
    
  
    $('#table1').dataTable( {
      "sPaginationType": "full_numbers",
      "aoColumns": [
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      { "asSorting": [ ] }
      ],
      "oLanguage": {
      "sLengthMenu": "每页显示 _MENU_ 条记录",
      "sZeroRecords": "抱歉， 没有找到",
      "sInfo": "从 _START_ 到 _END_ /共 _TOTAL_ 条数据",
      "sInfoEmpty": "没有数据",
      "sInfoFiltered": "(从 _MAX_ 条数据中检索)",
      "oPaginate": {
      "sFirst": "首页",
      "sPrevious": "前一页",
      "sNext": "后一页",
      "sLast": "尾页"
      },
      "sZeroRecords": "没有检索到数据",
      "sSearch": "搜索:",
      "sProcessing": "正在加载中..."

      }

      } );

    // Chosen Select
    jQuery("select").chosen({
      'min-width': '100px',
      'white-space': 'nowrap',
      disable_search_threshold: 10
    });
    
    // Delete row in a table
    jQuery('.delete-row').click(function(){
      var c = confirm("Continue delete?");
      if(c)
        jQuery(this).closest('tr').fadeOut(function(){
          jQuery(this).remove();
        });
        
        return false;
    });
    
  
  
  });