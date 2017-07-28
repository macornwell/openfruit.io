root = exports ? this
root.openfruit = root.openfruit ? {}
root.openfruit.common = root.openfruit.common ? {}




class RadioShow
  constructor: ()->
    @_radioToHidden = [];
    radioCollapses = $('.radio-show');
    radioCollapses.each((index)=>
      thisObj = $(radioCollapses[index])
      target = $(thisObj.attr('data-target'))
      @_radioToHidden.push([thisObj, target])
    )

    radioCollapses.on("change", ()=>
      for keyPair in @_radioToHidden
        key = keyPair[0];
        target = keyPair[1];
        if (key.is(':checked'))
          target.show();
        else
          target.hide();
    )


root.openfruit.common.RadioShow = RadioShow