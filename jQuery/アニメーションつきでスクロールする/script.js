$('a').click(function(){
  var $id = $(this).attr('href');
  var $position = $($id).offset().top; //position はピクセル数
  $('html, body').animate(
    {'scrollTop': $position},
    500 //ミリ秒
  );
});
