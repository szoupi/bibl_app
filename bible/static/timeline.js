window.onscroll = function changeClass() {
	
    var scrollPosY = window.pageYOffset
    {% for verseX in chapter.verse_set.all %}
                    console.log('scroll works ', '{{ verseX.number }}' );
                {% endfor %}
		
}
