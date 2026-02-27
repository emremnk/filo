document.addEventListener('DOMContentLoaded', async function () {
  const calendarEl = document.getElementById('calendar');
  const response = await fetch('/api/events');
  const events = await response.json();

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek'
    },
    locale: 'tr',
    events,
    dateClick(info) {
      const list = document.getElementById('eventList');
      list.innerHTML = '';
      const dayEvents = events.filter(e => e.date === info.dateStr);
      if (dayEvents.length === 0) {
        list.innerHTML = '<li class="list-group-item">Bu gün için olay yok.</li>';
      } else {
        dayEvents.forEach(ev => {
          const li = document.createElement('li');
          li.className = 'list-group-item';
          li.textContent = ev.title;
          list.appendChild(li);
        });
      }
      new bootstrap.Modal(document.getElementById('eventsModal')).show();
    }
  });

  calendar.render();
});
