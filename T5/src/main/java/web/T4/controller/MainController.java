package web.T4.controller;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Size;
import web.T4.service.MainService;

@Controller
public class MainController {
  @Autowired
  private MainService mainService;

  @GetMapping("/admin")
  public String admin(Model model) {
    return admin(1, model);
  }

  @GetMapping("/admin/page/{number}")
  public String admin(@PathVariable("number") @Min(1) Integer number, Model model) {
    List<Map<String, String>> archivosData = mainService.getArchivosData(number);

    Map<String, String> first = archivosData.get(0);
    if (first.get("left").equals("true")) {
      model.addAttribute("prev", number - 1);
    }
    if (first.get("right").equals("true")) {
      model.addAttribute("next", number + 1);
    }

    List<Map<String, String>> archivos = archivosData.subList(1, archivosData.size());
    if (archivos.isEmpty()) {
      return "redirect:/empty";
    }

    model.addAttribute("archivos", archivos);

    return "admin";
  }

  @GetMapping("/empty")
  @ResponseBody
  public String empty() {
    return "There's no data to show";
  }

  @GetMapping("/")
  public String index(Model model) {
    return "redirect:/page/1";
  }

  @GetMapping("/login")
  public String login() {
    return "login";
  }

  @GetMapping("/page/{number}")
  public String index(@PathVariable("number") @Min(1) Integer number, Model model) {
    List<Map<String, String>> dispositivosData = mainService.getDispositivosData(number);

    Map<String, String> first = dispositivosData.get(0);

    if (first.get("left").equals("true")) {
      model.addAttribute("prev", number - 1);
    }
    if (first.get("right").equals("true")) {
      model.addAttribute("next", number + 1);
    }

    List<Map<String, String>> dispositivos = dispositivosData.subList(1, dispositivosData.size());
    if (dispositivos.isEmpty()) {
      return "redirect:/empty";
    }

    model.addAttribute("dispositivos", dispositivos);
    return "interface";
  }

  @PostMapping("/update")
  public String update(@RequestParam("attr") @Size(max = 200, message = "Largo máximo 200") String attr,
      @RequestParam("id") Integer id) {
    mainService.updateDispositivo(id, attr);
    return "redirect:/";
  }

  @PostMapping("/admin/remove")
  public String remove(@RequestParam("id") Integer id, @RequestParam("msg") String msg, Model model) {
    mainService.RemoveArchivo(id, msg);
    model.addAttribute("msg", "Archivo eliminado");
    return admin(model);
  }
}
