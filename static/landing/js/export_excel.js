function test() {
	var array = [];
	var array_row = [];
	var value = $("#myInput").val().toLowerCase();

	$('#myTable tr').each(function () {
		$("#myTable tr").filter(function() {
			$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
		});

		if ($(this).css("display")!='none'){
			$(this).find('#id').each(function () {
				array_row.push($(this).text());
			});
			array.push(array_row);
		}
	});
	$('#report').val(array_row);
	array_row = encodeURIComponent(array_row)
}