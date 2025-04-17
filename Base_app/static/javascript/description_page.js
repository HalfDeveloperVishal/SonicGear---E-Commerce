function changeImage(thumb) {
    const mainImg = document.getElementById('main-product-image');
    mainImg.src = thumb.src;
  
    document.querySelectorAll('.thumbnail').forEach(img => img.classList.remove('active'));
    thumb.classList.add('active');
  }
  