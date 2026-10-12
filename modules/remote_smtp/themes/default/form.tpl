<div class="iss-form">
  <div class="iss-form__toolbar">
    <span class="iss-form__hint"><span class="iss-required">*</span> {$REQUIRED_FIELD}</span>
    <div class="iss-form__buttons">
      <input class="button" name="save" value="{$CONFIGURATION_UPDATE}" type="submit" />
    </div>
  </div>
  <section class="iss-card">
    <header class="iss-card__header"><i class="ti ti-mail-forward"></i> {$title}</header>
    <div class="iss-card__body iss-formgrid">
      <div class="iss-field">
        <span class="iss-field__label">{$status.LABEL}</span>
        <span class="iss-field__control">{$status.INPUT}</span>
      </div>
      <div class="iss-field">
        <span class="iss-field__label">{$SMTP_Server.LABEL}</span>
        <span class="iss-field__control">{$SMTP_Server.INPUT}</span>
      </div>
      <div class="iss-field">
        <span class="iss-field__label">{$relayhost.LABEL}&nbsp;<span class="iss-required">*</span></span>
        <span class="iss-field__control">{$relayhost.INPUT}</span>
      </div>
      <div class="iss-field">
        <span class="iss-field__label">{$port.LABEL}&nbsp;<span class="iss-required">*</span></span>
        <span class="iss-field__control">{$port.INPUT}</span>
      </div>
      <div class="iss-field">
        <span class="iss-field__label">{$user.LABEL}&nbsp;<span class="iss-required validpass">*</span></span>
        <span class="iss-field__control">
          <span class="iss-inline-field">
            <span>{$user.INPUT}</span>
            <span class="iss-field__help">({$Example}. <span id="example">example@domain.com</span>)</span>
          </span>
        </span>
      </div>
      <div class="iss-field">
        <span class="iss-field__label">{$password.LABEL}&nbsp;<span class="iss-required validpass">*</span></span>
        <span class="iss-field__control">{$password.INPUT}</span>
      </div>
      <div class="iss-field iss-field--full">
        <span class="iss-field__label">{$autentification.LABEL}</span>
        <span class="iss-field__control">{$autentification.INPUT}{$MSG_REMOTE_AUT}</span>
      </div>
      <div class="iss-field iss-field--full">
        <span class="iss-field__help">{$MSG_REMOTE_SMTP}</span>
      </div>
    </div>
  </section>
</div>

<input type="hidden" name="lbldomain" id="lbldomain" value="{$lbldomain}"/>
