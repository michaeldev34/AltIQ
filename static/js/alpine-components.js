/**
 * AltIQ Alpine.js Components
 * 
 * Reusable Alpine.js components for interactive UI elements.
 * Requires Alpine.js to be loaded before this script.
 * 
 * Components:
 * - dropdown: Click-to-toggle dropdown menus
 * - modal: Dialog/modal windows
 * - accordion: Expandable sections
 * - tabs: Tab navigation
 * - toast: Notification toasts
 */

document.addEventListener('alpine:init', () => {

  // Dropdown component
  Alpine.data('dropdown', () => ({
    open: false,

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    // Close on click outside
    init() {
      this.$watch('open', (value) => {
        if (value) {
          setTimeout(() => {
            document.addEventListener('click', this.handleClickOutside);
          }, 0);
        } else {
          document.removeEventListener('click', this.handleClickOutside);
        }
      });
    },

    handleClickOutside(e) {
      if (!this.$el.contains(e.target)) {
        this.close();
      }
    }
  }));

  // Modal component
  Alpine.data('modal', (initialOpen = false) => ({
    open: initialOpen,

    show() {
      this.open = true;
      document.body.style.overflow = 'hidden';
    },

    hide() {
      this.open = false;
      document.body.style.overflow = '';
    },

    toggle() {
      this.open ? this.hide() : this.show();
    },

    // Close on Escape key
    init() {
      this.$watch('open', (value) => {
        if (value) {
          document.addEventListener('keydown', this.handleEscape);
        } else {
          document.removeEventListener('keydown', this.handleEscape);
        }
      });
    },

    handleEscape(e) {
      if (e.key === 'Escape') {
        this.hide();
      }
    }
  }));

  // Accordion component
  Alpine.data('accordion', (allowMultiple = false) => ({
    activeItems: [],

    toggle(id) {
      if (this.isActive(id)) {
        this.activeItems = this.activeItems.filter(item => item !== id);
      } else {
        if (allowMultiple) {
          this.activeItems.push(id);
        } else {
          this.activeItems = [id];
        }
      }
    },

    isActive(id) {
      return this.activeItems.includes(id);
    }
  }));

  // Tabs component
  Alpine.data('tabs', (defaultTab = '') => ({
    activeTab: defaultTab,

    init() {
      // Set first tab as default if none specified
      if (!this.activeTab) {
        const firstTab = this.$el.querySelector('[data-tab]');
        if (firstTab) {
          this.activeTab = firstTab.dataset.tab;
        }
      }
    },

    select(tab) {
      this.activeTab = tab;
    },

    isActive(tab) {
      return this.activeTab === tab;
    }
  }));

  // Toast notifications
  Alpine.store('toasts', {
    items: [],

    add(message, type = 'info', duration = 4000) {
      const id = Date.now();
      this.items.push({ id, message, type });

      if (duration > 0) {
        setTimeout(() => this.remove(id), duration);
      }

      return id;
    },

    remove(id) {
      this.items = this.items.filter(item => item.id !== id);
    },

    success(message, duration) {
      return this.add(message, 'success', duration);
    },

    error(message, duration) {
      return this.add(message, 'error', duration);
    },

    warning(message, duration) {
      return this.add(message, 'warning', duration);
    }
  });

});

