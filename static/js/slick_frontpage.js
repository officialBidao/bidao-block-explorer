$('.testimonials').slick({
  infinite: true,
  slidesToShow: 3,
    dots: true,
  slidesToScroll: 1,
    arrows: false,

    responsive: [
    {
      breakpoint: 1154,
      settings: {
        centerPadding: '40px',
        slidesToShow: 2
      }
    },
    {
      breakpoint: 688,
      settings: {
        slidesToShow: 1
      }
    }
  ]
});
		