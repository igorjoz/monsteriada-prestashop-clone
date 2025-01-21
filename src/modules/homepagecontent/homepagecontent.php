<?php
if (!defined('_PS_VERSION_')) {
    exit;
}

class HomepageContent extends Module
{
    public function __construct()
    {
        $this->name = 'homepagecontent';
        $this->tab = 'front_office_features';
        $this->version = '1.0.0';
        $this->author = 'Igor Józefowicz';
        $this->need_instance = 0;

        parent::__construct();

        $this->displayName = $this->l('Homepage main content');
        $this->description = $this->l('Main content for homepage - custom HTML & CSS.');
    }

    public function install()
    {
        // return parent::install() && $this->registerHook('displayHomeContent');
        return parent::install() && $this->registerHook('displayHome');
    }

    public function uninstall()
    {
        return parent::uninstall();
    }

    public function hookDisplayHome($params)
    {
        // Add your custom CSS file
        $this->context->controller->addCSS($this->_path . 'views/css/homepagecontent.css');

        // Assign variables to Smarty (if needed)
        // $this->context->smarty->assign('variable', 'value');

        // Display the template file located in views/templates/hook/displayHome.tpl
        return $this->display(__FILE__, 'views/templates/hook/displayHome.tpl');
    }

    // public function hookDisplayHomeContent($params)
    // {
    //     $this->context->controller->addCSS($this->_path . 'views/css/homepagecontent.css');

    //     return $this->display(__FILE__, 'views/templates/hook/displayHomeContent.tpl');
    // }
}
