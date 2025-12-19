// onesignal.js
window.OneSignal = window.OneSignal || [];

OneSignal.push(function() {
  OneSignal.init({
    appId: "20670296-bbf3-4fe9-b176-9dedd50004ee",
    
    // Enable the notification button
    notifyButton: {
      enable: true,
      size: 'medium',
      position: 'bottom-right',
      showCredit: false,
      text: {
        'tip.state.unsubscribed': 'Subscribe to notifications',
        'tip.state.subscribed': "You're subscribed!",
        'tip.state.blocked': "You've blocked notifications",
        'message.prenotify': 'Click to subscribe to notifications',
        'message.action.subscribed': "Thanks for subscribing!",
        'message.action.resubscribed': "You're subscribed!",
        'message.action.unsubscribed': "You won't receive notifications again",
      }
    },
    
    // Welcome notification
    welcomeNotification: {
      title: "🎉 Welcome to LangChain Tutorials!",
      message: "You'll now get notified about new tutorials and updates.",
      url: "https://langchain-tutorials.github.io"
    },
    
    // Auto prompt settings
    autoRegister: false,
    autoResubscribe: true,
    
    // Slidedown prompt
    promptOptions: {
      slidedown: {
        enabled: true,
        autoPrompt: true,
        timeDelay: 10, // Wait 10 seconds before showing
        pageViews: 1,  // Show after 1 page view
        actionMessage: "Stay updated with the latest LangChain tutorials, guides, and AI development tips!",
        acceptButtonText: "Subscribe",
        cancelButtonText: "Maybe Later",
        categories: {
          tags: [
            {
              tag: "tutorials",
              label: "New Tutorials"
            },
            {
              tag: "updates",
              label: "Site Updates"
            }
          ]
        }
      }
    }
  });
  
  // Track subscription
  OneSignal.on('subscriptionChange', function(isSubscribed) {
    console.log("Subscription state changed: ", isSubscribed);
  });
});