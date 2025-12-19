/**
 * OneSignal Push Notification Setup
 * Can be easily migrated to FCM later
 */

window.OneSignal = window.OneSignal || [];

OneSignal.push(function() {
  OneSignal.init({
    appId: "20670296-bbf3-4fe9-b176-9dedd50004ee",
    
    // Notification settings
    allowLocalhostAsSecureOrigin: true,
    
    // Prompt settings
    notifyButton: {
      enable: true,
      size: 'medium',
      theme: 'default',
      position: 'bottom-right',
      offset: {
        bottom: '20px',
        right: '20px'
      },
      text: {
        'tip.state.unsubscribed': 'Subscribe for new tutorials',
        'tip.state.subscribed': "You're subscribed!",
        'tip.state.blocked': "You've blocked notifications",
        'message.prenotify': 'Click to subscribe',
        'message.action.subscribed': "Thanks for subscribing!",
        'message.action.resubscribed': "You're subscribed!",
        'dialog.main.title': 'Get Tutorial Updates',
        'dialog.main.button.subscribe': 'SUBSCRIBE',
        'dialog.blocked.title': 'Unblock Notifications',
        'dialog.blocked.message': "Follow these instructions to allow notifications:"
      }
    },
    
    // Welcome notification
    welcomeNotification: {
      title: "🎉 Welcome to LangChain Tutorials!",
      message: "You'll get notified when we publish new tutorials.",
      url: "https://langchain-tutorials.github.io"
    },
    
    // Prompt options
    promptOptions: {
      slidedown: {
        enabled: true,
        actionMessage: "Get notified about new LangChain tutorials and updates!",
        acceptButtonText: "ALLOW",
        cancelButtonText: "NO THANKS"
      }
    }
  });
});

// Optional: Track subscription
OneSignal.push(function() {
  OneSignal.on('subscriptionChange', function(isSubscribed) {
    console.log("Subscription changed:", isSubscribed);
  });
});