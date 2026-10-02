const form = document.querySelector('#order-form');
const status = document.querySelector('.form-status');
const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

document.querySelector('#year').textContent = new Date().getFullYear();

menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('nav-open', open);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('nav-open');
  menuButton.setAttribute('aria-expanded', 'false');
}));

form.addEventListener('submit', async event => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const values = Object.fromEntries(new FormData(form).entries());
  const button = form.querySelector('[type="submit"]');
  button.disabled = true;
  button.innerHTML = 'Preparing your enquiry <span>…</span>';
  status.textContent = '';
  try {
    const response = await fetch('/api/enquiries', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(values)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'We could not save this enquiry. Please try again.');
    const lines = [
      'Hello KGF Bricks Suppliers, I would like to enquire about bricks.', '',
      `Name: ${values.name}`, `Phone: ${values.phone}`, `Delivery area: ${values.area}`,
      `Quantity: ${values.quantity}`, `Delivery address / landmark: ${values.address}`,
      values.preferred_date ? `Preferred delivery date: ${values.preferred_date}` : '',
      values.notes ? `Other requirements: ${values.notes}` : '', '',
      'Please confirm current price, availability, delivery charges and timing.'
    ].filter(Boolean);
    status.textContent = `Enquiry #${result.id} saved. Opening WhatsApp so you can review and send your message.`;
    window.open(`https://wa.me/919603804243?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener,noreferrer');
  } catch (error) {
    status.textContent = `${error.message} You can call 96038 04243 instead.`;
  } finally {
    button.disabled = false;
    button.innerHTML = 'Send enquiry on WhatsApp <span>↗</span>';
  }
});
