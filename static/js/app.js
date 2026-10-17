(() => {
  "use strict";
  const CART_KEY = "foodie_demo_cart_v1";
  const readCart = () => {
    try { return JSON.parse(localStorage.getItem(CART_KEY) || "[]"); }
    catch { return []; }
  };
  const saveCart = cart => {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartCount();
  };
  const updateCartCount = () => {
    const count = readCart().reduce((sum, item) => sum + Number(item.qty || 0), 0);
    document.querySelectorAll("[data-cart-count]").forEach(node => node.textContent = count);
  };
  const format = n => "₹" + Number(n).toLocaleString("en-IN");
  const mergeItem = incoming => {
    let cart = readCart();
    const incomingRestaurant = Number(incoming.restaurantId);
    if (cart.length && Number(cart[0].restaurantId) !== incomingRestaurant) {
      cart = [];
      const notice = document.getElementById("pending-cart-notice");
      if (notice) notice.textContent = "You are logged in. Your selected item has been added; the old cart was cleared because this demo supports one restaurant per order.";
    }
    const current = cart.find(item => Number(item.id) === Number(incoming.id));
    if (current) current.qty = Math.min(50, Number(current.qty || 0) + Number(incoming.qty || 1));
    else cart.push({
      id: Number(incoming.id), name: String(incoming.name), price: Number(incoming.price),
      qty: Number(incoming.qty || 1), restaurantId: incomingRestaurant
    });
    saveCart(cart);
  };

  // If a guest selected Add, the server stores the pending item while the user logs in.
  // After successful login, the detail page passes that item here once for the cart.
  const pendingNode = document.getElementById("pending-cart-item");
  if (pendingNode) {
    try {
      const pending = JSON.parse(pendingNode.textContent);
      if (pending && pending.id) {
        mergeItem(pending);
        const notice = document.getElementById("pending-cart-notice");
        if (notice && !notice.textContent.includes("old cart was cleared")) notice.textContent = "You're logged in — " + pending.name + " has been added to your cart.";
      }
    } catch (error) { console.warn("Could not restore selected cart item.", error); }
  }

  document.querySelectorAll("[data-add-item]").forEach(button => {
    button.addEventListener("click", () => {
      const incoming = {
        id: button.dataset.id, name: button.dataset.name, price: button.dataset.price,
        restaurantId: button.dataset.restaurant, qty: 1
      };
      let cart = readCart();
      if (cart.length && Number(cart[0].restaurantId) !== Number(incoming.restaurantId)) {
        const proceed = window.confirm("This demo supports one restaurant per order. Clear your current cart and add this item?");
        if (!proceed) return;
        cart = [];
        saveCart(cart);
      }
      mergeItem(incoming);
      const original = button.textContent;
      button.textContent = "ADDED ✓";
      button.disabled = true;
      window.setTimeout(() => { button.textContent = original; button.disabled = false; }, 850);
    });
  });

  const checkoutItems = document.getElementById("checkout-cart-items");
  if (checkoutItems) {
    const cart = readCart();
    checkoutItems.innerHTML = "";
    if (!cart.length) {
      checkoutItems.innerHTML = '<p class="muted">Your cart is empty. <a class="text-link" href="/#restaurants">Explore restaurants</a></p>';
    } else {
      cart.forEach(item => {
        const row = document.createElement("div"); row.className = "summary-row cart-line";
        const label = document.createElement("span"); label.textContent = `${item.qty} × ${item.name}`;
        const price = document.createElement("strong"); price.textContent = format(Number(item.price) * Number(item.qty));
        row.append(label, price); checkoutItems.appendChild(row);
      });
    }
    const subtotal = cart.reduce((sum, item) => sum + Number(item.price) * Number(item.qty), 0);
    const subtotalEl = document.getElementById("cart-subtotal");
    if (subtotalEl) subtotalEl.textContent = format(subtotal);
    const payload = document.getElementById("cart-payload");
    if (payload) payload.value = JSON.stringify(cart.map(item => ({id: item.id, qty: item.qty})));
    const form = document.getElementById("checkout-form");
    if (form) form.addEventListener("submit", event => {
      const latestCart = readCart();
      if (!latestCart.length) {
        event.preventDefault();
        window.alert("Your cart is empty. Open a restaurant menu and add a dish first.");
        return;
      }
      if (payload) payload.value = JSON.stringify(latestCart.map(item => ({id: item.id, qty: item.qty})));
    });
  }

  if (document.body.dataset.clearCart === "1") {
    localStorage.removeItem(CART_KEY);
  }
  updateCartCount();
})();
