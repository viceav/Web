package web.T4.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import jakarta.validation.constraints.Min;
import web.T4.data.Dispositivo;
import web.T4.data.DispositivoRepository;

@Controller
public class MainController {
  @Autowired
  private DispositivoRepository dv;

  @GetMapping("/")
  public String index(Model model) {
    return index(1, model);
  }

  @GetMapping("/page/{number}")
  public String index(@PathVariable("number") @Min(1) Integer number, Model model) {
    Page<Dispositivo> dispositivos = dv.findAll(PageRequest.of(number - 1, 10));

    if (dispositivos.isEmpty()) {
      return "redirect:/";
    }
    if (dispositivos.hasNext()) {
      model.addAttribute("next", number + 1);
    }
    if (dispositivos.hasPrevious()) {
      model.addAttribute("prev", number - 1);
    }

    List<Map<String, String>> dispositivosData = new ArrayList<>();

    for (Dispositivo dis : dispositivos) {
      Map<String, String> disData = new HashMap<>();
      putData(dis, disData);

      dispositivosData.add(disData);
    }

    model.addAttribute("dispositivos", dispositivosData);
    return "interface";
  }

  private void putData(Dispositivo dis, Map<String, String> disData) {
    disData.put("id", dis.getId().toString());
    disData.put("nombre", dis.getNombre().toString());
    disData.put("anos_uso", dis.getAnos_uso().toString());
    disData.put("tipo", dis.getTipo().toString().toLowerCase());
    disData.put("estado", dis.getEstado().toString().replace("_", " ").toLowerCase());
    disData.put("me_gusta", dis.getContador_megusta().toString());
    disData.put("no_me_gusta", dis.getContador_nomegusta().toString());
  }

  @PostMapping("/update")
  public String update(@RequestParam("attr") String attr, @RequestParam("id") Integer id) {
    try {
      Dispositivo dis = dv.findById(id).get();
      if ("me_gusta".equals(attr)) {
        dis.setContador_megusta(dis.getContador_megusta() + 1);
      } else if ("no_me_gusta".equals(attr)) {
        dis.setContador_nomegusta(dis.getContador_nomegusta() + 1);
      }
      dv.save(dis);
      return "redirect:/";
    } catch (Exception e) {
      return "redirect:/";
    }
  }

}
