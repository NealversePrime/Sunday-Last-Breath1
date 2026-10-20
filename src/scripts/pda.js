// Function to trigger the PDA Dialog box
window.openPDA = function() {
    var pdaPassage = Story.get("PDA_Overlay");
    if (!pdaPassage) {
        console.error("PDA_Overlay passage not found!");
        return;
    }
    Dialog.setup("SURVIVOR PDA", "pda-dialog");
    Dialog.wiki(pdaPassage.text);
    Dialog.open();
};

// Prevent default tab behavior (element focus cycling) unless in text inputs
$(document).on('keydown', function (e) {
    if (e.key === 'Tab' && !$(e.target).is('input, textarea, select')) {
        e.preventDefault();
    }
});

// Bind the TAB key to open/close the menu instantly
$(document).on('keyup', function (e) {
    if (e.key === 'Tab') {
        if ($(e.target).is('input, textarea, select')) {
            return;
        }
        e.preventDefault();
        
        // If a dialog is already open, close it. Otherwise, open the PDA.
        if ($("#ui-dialog-dialog").is(":visible")) {
            Dialog.close();
        } else {
            window.openPDA();
        }
    }
});
