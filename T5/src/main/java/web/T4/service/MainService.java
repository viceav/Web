package web.T4.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import jakarta.transaction.Transactional;
import web.T4.data.Archivo;
import web.T4.data.ArchivoRepository;
import web.T4.data.Dispositivo;
import web.T4.data.DispositivoRepository;
import web.T4.data.Log;
import web.T4.data.LogRepository;

@Service
public class MainService {
  @Autowired
  private DispositivoRepository dv;

  @Autowired
  private ArchivoRepository ar;

  @Autowired
  private LogRepository lr;

  public List<Map<String, String>> getArchivosData(Integer number) {
    Page<Archivo> archivos = ar
        .findAll(PageRequest.of(number - 1, 10, Sort.by("dispositivo.contacto.fecha").descending()));

    List<Map<String, String>> archivosData = new ArrayList<>();
    String left = "none";
    String right = "none";

    if (archivos.hasNext()) {
      right = "true";
    }
    if (archivos.hasPrevious()) {
      left = "true";
    }

    archivosData.add(Map.of("left", left, "right", right));

    for (Archivo arch : archivos) {
      Map<String, String> archData = new HashMap<>();
      archData.put("id", arch.getId().toString());
      archData.put("ruta", arch.getRuta_archivo());
      Dispositivo dis = arch.getDispositivo();
      archData.put("dis", dis.getNombre());
      archData.put("con", dis.getContacto().getEmail());

      archivosData.add(archData);
    }

    return archivosData;
  }

  public List<Map<String, String>> getDispositivosData(Integer number) {
    Page<Dispositivo> dispositivos = dv.findAll(PageRequest.of(number - 1, 10));

    List<Map<String, String>> dispositivosData = new ArrayList<>();

    String left = "none";
    String right = "none";

    if (dispositivos.hasNext()) {
      right = "true";
    }
    if (dispositivos.hasPrevious()) {
      left = "true";
    }

    dispositivosData.add(Map.of("left", left, "right", right));

    for (Dispositivo dis : dispositivos) {
      Map<String, String> disData = new HashMap<>();
      disData.put("id", dis.getId().toString());
      disData.put("nombre", dis.getNombre().toString());
      disData.put("anos_uso", dis.getAnos_uso().toString());
      disData.put("tipo", dis.getTipo().toString().toLowerCase());
      disData.put("estado", dis.getEstado().toString().replace("_", " ").toLowerCase());
      disData.put("me_gusta", dis.getContador_megusta().toString());
      disData.put("no_me_gusta", dis.getContador_nomegusta().toString());

      dispositivosData.add(disData);
    }

    return dispositivosData;
  }

  public Boolean updateDispositivo(Integer id, String attr) {
    try {
      Dispositivo dis = dv.findById(id).get();
      if ("me_gusta".equals(attr)) {
        dis.setContador_megusta(dis.getContador_megusta() + 1);
      } else if ("no_me_gusta".equals(attr)) {
        dis.setContador_nomegusta(dis.getContador_nomegusta() + 1);
      }
      dv.save(dis);
      return false;
    } catch (Exception e) {
      return true;
    }
  }

  @Transactional
  public void RemoveArchivo(Integer id, String msg) {
    ar.deleteById(id);
    registerLog(id, msg);
  }

  private void registerLog(Integer id, String msg) {
    Log log = new Log();
    msg = "Eliminado archivo " + id + " por usuario admin, motivo: " + msg;
    log.setMensaje(msg);
    lr.save(log);
  }
}
