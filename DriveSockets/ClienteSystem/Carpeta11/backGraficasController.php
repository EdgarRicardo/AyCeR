<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

use DB;

use App\Models\Cms\Noticia;
use App\Models\Cms\Candidato;
use App\Models\Cms\Estado;
use App\Models\Cms\Encuestadora;
use App\Models\Cms\PartidoPolitico;
use App\Models\Cms\VotoMunicipio;
use App\Models\Cms\VotoCongreso;
use App\Models\Cms\Municipio;
use App\Models\Cms\EncuestaEstado;
use App\Models\Cms\EncuestaAprobacion;
use App\Models\Cms\EncuestaCongreso;
use App\Models\Cms\EncuestaMunicipio;
use App\Models\Cms\VotoEstado;




class GraficasController extends Controller
{
   // 04/01/2021
    public function getGraficaCamaraDiputados(Request $request){

        $anio_eleccion  =  VotoCongreso::select('anio_eleccion','fecha')
        ->where('titulo','2021')
        ->groupBy('anio_eleccion')
        ->orderBy('anio_eleccion', 'desc')->first();

        $votoCongreso  =  VotoCongreso::select('votos_congreso.fecha','pp.abreviacion as name','votos_congreso.porcenjate_votos as data', 'pp.color as color')
        ->join('partidos_politicos as pp','pp.id','votos_congreso.partido_politico_id')
        ->where('votos_congreso.porcenjate_votos','>',0)
        ->where('votos_congreso.anio_eleccion',$anio_eleccion->anio_eleccion)
        ->where('titulo','2021')
        ->get();
            $partidoCurules=[];
            $colores=[];

      foreach ($votoCongreso as $key => $congreso) {
        array_push($partidoCurules,[$congreso->name,ceil($congreso->data),$congreso->color,$congreso->name]);
        // array_push($colores,$congreso->color);
      }
         return response()->json([
            'jsonVotoCongreso' => $partidoCurules,
            'fecha'            => $anio_eleccion->fecha
        ]);
    }

    public function getGraficaCamaraDiputadosAnios(Request $request){


        $anio    = $request->input('fecha');

        $votoCongreso  =  VotoCongreso::select('pp.abreviacion as name','votos_congreso.porcenjate_votos as data', 'pp.color as color')
        ->join('partidos_politicos as pp','pp.id','votos_congreso.partido_politico_id')
        ->where('votos_congreso.porcenjate_votos','>',0)
        ->where('votos_congreso.titulo',$anio)
        ->whereNotIn('pp.abreviacion',['NINGUNO','NS/NC'])
        ->get();

            $partidoCurules=[];
            $colores=[];

            foreach ($votoCongreso as $key => $congreso) {
                array_push($partidoCurules,[$congreso->name,ceil($congreso->data),$congreso->color,$congreso->name]);
              }
                 return response()->json([
                    'jsonVotoCongreso' => $partidoCurules
                ]);

    }


    public function getGraficaCamaraDiputadosBarras(Request $request){

        $anio_eleccion  =  VotoCongreso::select('anio_eleccion','fecha')
        ->where('titulo','2021')
        ->groupBy('anio_eleccion')
        ->orderBy('anio_eleccion', 'desc')->first();

        $votoCongresoBarras  =  VotoCongreso::select('votos_congreso.fecha','pp.abreviacion as name','votos_congreso.porcenjate_votos as data', 'pp.color as color')
        ->join('partidos_politicos as pp','pp.id','votos_congreso.partido_politico_id')
        ->where('votos_congreso.anio_eleccion',$anio_eleccion->anio_eleccion)
        ->where('votos_congreso.porcenjate_votos','>',0)
        ->where('titulo','2021')
        ->get();

       $partidoCurules=[];

      foreach ($votoCongresoBarras as $key => $congreso) {

        $obj = (object) array(
            'name'  => $congreso->name,
            'data'  => [$congreso->data],
            'color' => $congreso->color,
            'y'     => $congreso->data
        );
            array_push($partidoCurules,$obj);
      }

         return response()->json([
            'partidoCurules' => $partidoCurules,
            'fecha'          => $anio_eleccion->fecha

        ]);

    }

    public function getTablaEncuestadora(Request $request)
    {
        $id_encuestadora    = $request->input('id_encuestadora');

        $partidos       = PartidoPolitico::All();
        $auxiliar=array();
        foreach ($partidos as $key => $partido) {

            $datosEncuesta = EncuestaCongreso::select('encuestas_congresos.fecha','pp.abreviacion as nombre','encuestas_congresos.porcenjate_votos as porcentaje','pp.color','pp.logo')
            ->join('partidos_politicos as pp','pp.id','encuestas_congresos.partido_politico_id')
            ->where('encuestas_congresos.encuestadora_id',$id_encuestadora )
            ->where('encuestas_congresos.porcenjate_votos','>',0)
            ->where('encuestas_congresos.partido_politico_id',$partido->id)
            ->orderBy('encuestas_congresos.fecha', 'desc')->first();

            if($datosEncuesta!=null){
            array_push($auxiliar,$datosEncuesta);
            }
        }

        $fecha = EncuestaCongreso::select(DB::raw('DATE_FORMAT(encuestas_congresos.fecha, "%m-%Y") as fecha')
        )
        ->join('partidos_politicos as pp','pp.id','encuestas_congresos.partido_politico_id')
        ->where('encuestas_congresos.encuestadora_id',$id_encuestadora)
        ->groupBy('encuestas_congresos.fecha')->first();

        return response()->json([
            'auxiliar' => $auxiliar,
            'fecha'   =>$fecha
            ]);

    }

    public function  getCandidatosEstado (Request $request)
    {

        $id_estado = $request->input('id_estado');

        $fechaMasActual  = DB::table('votos_estado')
        ->where('votos_estado.estado_id',$id_estado)->get()
        ->max('fecha');

        $votos = VotoEstado::select('votos_estado.fecha','pp.abreviacion','pp.logo','pp.color','votos_estado.porcenjate_votos')
        ->join('estados as e','e.id','votos_estado.estado_id')
        ->join('partidos_politicos as pp','pp.id','votos_estado.partido_politico_id')
        ->where('votos_estado.estado_id',$id_estado)
        ->where('votos_estado.fecha',$fechaMasActual)
        ->where('votos_estado.porcenjate_votos','>',0)
        ->distinct()
        ->get();
        $candidatos=[];
        if(in_array($id_estado,[32,24.16]))
        $candidatos=Candidato::select('candidatos.nombre','candidatos.foto','pp.logo','pp.abreviacion')
            ->join('partidos_politicos as pp', 'pp.id' ,'candidatos.partido_politico_id')
            ->where('estado_id', $id_estado)
            ->where('anio_eleccion',date("Y"))
            ->get();

        $cand = [];
        foreach ($candidatos as $key => $c)
            if(!array_key_exists($c->abreviacion,$cand))
                $cand[$c->abreviacion] = [
                    "foto" => $c->foto,
                    "nombre" => $c->nombre."<br>".$c->abreviacion
                ];
        //$cand = [];
        foreach ($votos as $key => $v)
            if (array_key_exists($v->abreviacion,$cand)){
                $v->logo = $cand[$v->abreviacion]["foto"];
                $v->abreviacion = $cand[$v->abreviacion]["nombre"];
            }

        return response()->json([
            'candidatos' => $votos
        ]);

    }


    public function getTablaEncuestadoraEstados(Request $request){
        $id_encuestadora    = $request->input('id_encuestadora');
        $id_estado          = $request->input('id_estado');

        $partidos    = PartidoPolitico::All();
        $datos          = array();
        $datosPartidos  = array();
        $auxiliar=array();
        foreach ($partidos as $key => $partido) {

            $datosEncuesta = EncuestaEstado::select('encuestas_estados.fecha','pp.abreviacion as nombre','encuestas_estados.porcentaje_votos as porcentaje','pp.color','pp.logo')
            ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
            ->where('encuestas_estados.estado_id',$id_estado )
            ->where('encuestas_estados.porcentaje_votos','>',0 )
            ->where('encuestas_estados.encuestadora_id',$id_encuestadora )
            ->where('encuestas_estados.partido_politico_id',$partido->id)->orderBy('encuestas_estados.fecha', 'desc')->first();

            if($datosEncuesta!=null){
            array_push($auxiliar,$datosEncuesta);

            }
        }

        $fecha = EncuestaEstado::select(DB::raw('DATE_FORMAT(encuestas_estados.fecha, "%m-%Y") as fecha'))
        ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
        ->where('encuestas_estados.estado_id',$id_estado )
        ->where('encuestas_estados.encuestadora_id',$id_encuestadora )
        ->groupBy('encuestas_estados.fecha')->first();


        return response()->json([
            'auxiliar' => $auxiliar,
            'fecha'   =>$fecha
             ]);

    }


    public function getGraficaAlcaldia(Request $request){

        $id_alcaldia    = $request->input('id_alcaldia');

        $fechaMasActual  = DB::table('votos_municipios')
        ->where('votos_municipios.municipio_id',$id_alcaldia)->get()
        ->max('fecha');

        $votos  = VotoMunicipio::select('votos_municipios.fecha','pp.abreviacion','votos_municipios.porcenjate_votos', 'pp.color','pp.logo')
        ->join('partidos_politicos as pp','pp.id','votos_municipios.partido_politico_id')
        ->where('votos_municipios.porcenjate_votos','>',0 )
        ->where('votos_municipios.fecha',$fechaMasActual)
        ->where('votos_municipios.municipio_id',$id_alcaldia)->get();

        $candidatos=Candidato::select('candidatos.nombre','candidatos.foto','pp.logo','pp.abreviacion')
        ->join('partidos_politicos as pp', 'pp.id' ,'candidatos.partido_politico_id')
        ->where('municipio_id', $id_alcaldia)
        ->where('anio_eleccion',date("Y"))
        ->get();


        $cand = [];
        foreach ($candidatos as $key => $c)
            if(!array_key_exists($c->abreviacion,$cand))
                $cand[$c->abreviacion] = [
                    "foto" => $c->foto,
                    "nombre" => $c->nombre."<br>".$c->abreviacion
                ];
        $cand = [];
        foreach ($votos as $key => $v)
            if (array_key_exists($v->abreviacion,$cand)){
                $v->logo = $cand[$v->abreviacion]["foto"];
                $v->abreviacion = $cand[$v->abreviacion]["nombre"];
            }

        return response()->json([
            'candidatos' => $votos
        ]);

    }

    public function getAlcaldias(Request $request){

        $alcaldias  =  Municipio::where('estado_id',9)->get();

        return response()->json([
            'alcaldias' => $alcaldias
        ]);

    }

    public function getEncuestadoras(Request $request){
        $encuestadorasPolls  =  EncuestaEstado::select('e.id','e.nombre')
        ->join('encuestadoras as e','e.id','encuestas_estados.encuestadora_id')
        ->get();

        return response()->json([
            'encuestadorasPolls' => $encuestadorasPolls
        ]);

    }


    public function getPollofPollsDispersionAprobacion(Request $request)
    {
        $estimacionArray=array();
        $encuestadora='estimacion';

        $arrayNecesarioLineal=array();
        $arrayNecesarioDispersion=array();

            $estimaciones= EncuestaAprobacion::select('encuestas_aprobaciones.fecha','encuestas_aprobaciones.porcenjate_aprobado as aprobacion','encuestas_aprobaciones.porcenjate_desaprobado as desaprobaciones')
            ->join('encuestadoras as e','e.id','encuestas_aprobaciones.encuestadora_id')
            ->where('e.nombre',$encuestadora)->get();

            $fechas= EncuestaAprobacion::select(DB::raw('encuestas_aprobaciones.fecha as fecha'))
            ->join('encuestadoras as e','e.id','encuestas_aprobaciones.encuestadora_id')
            ->where('e.nombre',$encuestadora)->get();


            $fechaArray=array();
            foreach ($fechas as $key => $fecha) {
                setlocale(LC_ALL,"es_ES");
                date_default_timezone_set('America/Mexico_City');
                // Unix
                setlocale(LC_TIME, 'es_ES.UTF-8');
                // En windows
                setlocale(LC_TIME, 'spanish');
                $nuevaF=strftime("%b'%y", strtotime($fecha->fecha));
                $fechaSinPunto = str_replace (".",' ',$nuevaF);
                array_push($fechaArray,strtoupper ($fechaSinPunto));
            }
                $datosAprobaciones=array();
                $datosDesaprobaciones=array();

                foreach ($estimaciones as $key => $estimacion) {
                    array_push($datosAprobaciones   ,$estimacion->aprobacion);
                    array_push($datosDesaprobaciones,$estimacion->desaprobaciones);
                }

                $objA = (object) array(
                    'nombre'     => 'Aprobación',
                    'promedios'  =>  $datosAprobaciones,
                    'color'      =>  '#582E82'
                );

                $objD = (object) array(
                    'nombre'     => 'Desaprobación',
                    'promedios'  => $datosDesaprobaciones,
                    'color'      => '#00FCFC'
                );

                array_push($arrayNecesarioLineal,$objA);
                array_push($arrayNecesarioLineal,$objD);


            $aprobacionesPreDes= EncuestaAprobacion::select('encuestas_aprobaciones.fecha','encuestas_aprobaciones.porcenjate_aprobado as aprobacion','encuestas_aprobaciones.porcenjate_desaprobado as desaprobaciones')
            ->join('encuestadoras as e','e.id','encuestas_aprobaciones.encuestadora_id')
            ->where('e.nombre','!=',$encuestadora)->get();

            $encuestadorasArray=array();


                foreach ($aprobacionesPreDes as $j => $aprobaciones) {



                    foreach ($estimaciones as $i => $estimacion) {

                        if($estimacion->fecha==$aprobaciones->fecha){
                            $auxiliar=[$i,$aprobaciones->aprobacion];
                            array_push($encuestadorasArray,$auxiliar);
                        }else{
                            $auxiliar=[];
                            array_push($estimacionArray,$auxiliar);
                        }

                    }

                }

                $obj2 = (object) array(
                    'estatus'     => '',
                    'porcentaje'  =>  $encuestadorasArray,
                    'color'       =>  '#582E82'
                );

                array_push($arrayNecesarioDispersion,$obj2);


                $encuestadorasArray2=array();

                foreach ($aprobacionesPreDes as $j => $aprobaciones) {

                    foreach ($estimaciones as $i => $estimacion) {

                        if($estimacion->fecha==$aprobaciones->fecha){
                            $auxiliar2=[$i,$aprobaciones->desaprobaciones];
                            array_push($encuestadorasArray2,$auxiliar2);
                        }else{
                            $auxiliar2=[];
                            array_push($estimacionArray,$auxiliar2);
                        }

                    }

                }

                $obj3 = (object) array(
                    'estatus'     => '',
                    'porcentaje'  =>  $encuestadorasArray2,
                    'color'       =>  '#00FCFC'
                );

                array_push($arrayNecesarioDispersion,$obj3);



        return response()->json([
            'lineal'           => $arrayNecesarioLineal,
            'dispersion'       => $arrayNecesarioDispersion,
            'fechasDispersion' => $fechaArray,
            ]);

    }


    public function getGraficaAprobacionesPollofPolls(Request $request){

        $id_encuestadora    = $request->input('id_encuestadora');

        $aprobacionDesaprobacion  =  EncuestaAprobacion::select('porcenjate_aprobado as aprobacion','.porcenjate_desaprobado as desaprobacion','fecha')->where('encuestadora_id',$id_encuestadora)->get();

        $aprobaciones  =[];
        $desaprobacion =[];
        $fechas        =[];



      foreach ($aprobacionDesaprobacion as $key => $datos) {
          array_push($aprobaciones,$datos->aprobacion);
          array_push($desaprobacion,$datos->desaprobacion);

          setlocale(LC_ALL,"es_ES");
          date_default_timezone_set('America/Mexico_City');
          // Unix
          setlocale(LC_TIME, 'es_ES.UTF-8');
          // En windows
          setlocale(LC_TIME, 'spanish');
          $nuevaF=strftime("%b'%y", strtotime($datos->fecha));
          $fechaSinPunto = str_replace (".",' ',$nuevaF);
          array_push($fechas,strtoupper ($fechaSinPunto));
      }

         return response()->json([
            'aprobaciones' => $aprobaciones,
            'desaprobacion' => $desaprobacion,
            'fechas' => $fechas
        ]);

    }


    public function getDispersionCamara(Request $request)
    {

        $partidos= PartidoPolitico::All();

        $arrayDatosPartidos=array();
        $arrayDatosGrafica=array();

        $estimacionArray=array();
        $encuestadora='estimacion';

        $arrayNecesarioLineal=array();
        $arrayNecesarioDispersion=array();

        foreach ($partidos as $key => $partido) {

            $estimaciones = EncuestaCongreso::select('pp.nombre','encuestas_congresos.porcenjate_votos as porcentaje','pp.color','encuestas_congresos.fecha as fecha')
            ->join('partidos_politicos as pp','pp.id','encuestas_congresos.partido_politico_id')
            ->join('encuestadoras as e','e.id','encuestas_congresos.encuestadora_id')
            ->where('e.nombre',$encuestadora)
            ->where('encuestas_congresos.partido_politico_id',$partido->id)->get();


            if(count($estimaciones)!=0){

                $datosEstimacion=array();
                $fechas          =array();

                foreach($estimaciones as $key => $estimacion){

                    setlocale(LC_ALL,"es_ES");
                    date_default_timezone_set('America/Mexico_City');
                    // Unix
                    setlocale(LC_TIME, 'es_ES.UTF-8');
                    // En windows
                    setlocale(LC_TIME, 'spanish');
                    $nuevaF=strftime("%b'%y", strtotime($estimacion->fecha));
                    $fechaSinPunto = str_replace (".",' ',$nuevaF);
                    array_push($fechas,strtoupper ($fechaSinPunto));


                    array_push($datosEstimacion,floatval(number_format($estimacion->porcentaje,2)));
                }

                $obj = (object) array(
                    'nombre'  => $partido->abreviacion,
                    'promedios'  => $datosEstimacion,
                    'color' => $partido->color
                );
                 array_push($arrayNecesarioLineal,$obj);
            }

        }


        foreach ($partidos as  $partido) {

            $estimaciones = EncuestaCongreso::select('encuestas_congresos.fecha','pp.nombre','encuestas_congresos.porcenjate_votos as porcentaje','pp.color')
            ->join('partidos_politicos as pp','pp.id','encuestas_congresos.partido_politico_id')
            ->join('encuestadoras as e','e.id','encuestas_congresos.encuestadora_id')
            ->where('e.nombre',$encuestadora)
            ->where('encuestas_congresos.partido_politico_id',$partido->id)->get();

            $encuestadoras = EncuestaCongreso::select('encuestas_congresos.fecha','pp.nombre','encuestas_congresos.porcenjate_votos as porcentaje','pp.color')
            ->join('partidos_politicos as pp','pp.id','encuestas_congresos.partido_politico_id')
            ->join('encuestadoras as e','e.id','encuestas_congresos.encuestadora_id')
            ->where('e.nombre','!=',$encuestadora)
            ->where('encuestas_congresos.partido_politico_id',$partido->id)->get();
            $encuestadorasArray=array();

            if( count($encuestadoras) >0 ){


                foreach ($encuestadoras as $j => $encuestadoraVar) {

                    foreach ($estimaciones as $i => $estimacion) {

                        if($estimacion->fecha==$encuestadoraVar->fecha){
                            $auxiliar=[$i,floatval(number_format($encuestadoraVar->porcentaje,2))];
                            array_push($encuestadorasArray,$auxiliar);
                        }else{
                            $auxiliar=[];
                            array_push($estimacionArray,$auxiliar);
                        }

                    }

                }

                $obj2 = (object) array(
                    'estatus'  => $partido->abreviacion,
                    'porcentaje'  => $encuestadorasArray,
                    'color' => $partido->color
                );

                array_push($arrayNecesarioDispersion,$obj2);

            }

        }

        return response()->json([
            'lineal' => $arrayNecesarioLineal,
            'dispersion' => $arrayNecesarioDispersion,
            'fechasDispersion' => $fechas
            ]);


    }



    public function getPollofPolls(Request $request)
    {
        $id_encuestadora    = $request->input('id_encuestadora');

        $partidos= PartidoPolitico::All();

        $arrayDatosPartidos=array();
        $arrayDatosGrafica=array();
        $fechas          =array();
        foreach ($partidos as $key => $partido) {
            $auxiliar=array();

            $datosEncuesta = EncuestaCongreso::select('pp.nombre','encuestas_congresos.porcenjate_votos as porcentaje','pp.color','encuestas_congresos.fecha as fecha')
            ->join('partidos_politicos as pp','pp.id','encuestas_congresos.partido_politico_id')
            ->where('encuestas_congresos.encuestadora_id',$id_encuestadora )
            ->where('encuestas_congresos.partido_politico_id',$partido->id)->get();


            if(count($datosEncuesta)!=0){
                foreach($datosEncuesta as $key => $datos){
                    array_push($auxiliar,floatval(number_format($datos->porcentaje,2)));

                    setlocale(LC_ALL,"es_ES");
                    date_default_timezone_set('America/Mexico_City');
                    // Unix
                    setlocale(LC_TIME, 'es_ES.UTF-8');
                    // En windows
                    setlocale(LC_TIME, 'spanish');
                    $nuevaF=strftime("%b'%y", strtotime($datos->fecha));
                    $fechaSinPunto = str_replace (".",' ',$nuevaF);
                    array_push($fechas,strtoupper ($fechaSinPunto));
                }



                 array_push($arrayDatosGrafica,$auxiliar);
                    $obj = (object) array(
                        'name' => $partido->abreviacion,
                        'data' => $auxiliar,
                        'color' => $partido->color
                    );
                 array_push($arrayDatosPartidos,$obj);
            }

        }

        return response()->json([
            'polls' => $arrayDatosPartidos,
            'fechasDispersion' => $fechas
            ]);

    }


    public function getPollofPollsDispersionEstados(Request $request)
    {
        setlocale(LC_ALL,"es_ES");

        $id_estado          = $request->input('id_estado');

        $partidos= PartidoPolitico::All();

        $arrayDatosPartidos=array();
        $arrayDatosGrafica=array();

        $estimacionArray=array();
        $encuestadora='estimacion';

        $arrayNecesarioLineal     =array();
        $arrayNecesarioDispersion =array();
        $fechas                   =array();



        $fechasDatos= EncuestaEstado::select('encuestas_estados.fecha as fecha')
        ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
         ->join('encuestadoras as e','e.id','encuestas_estados.encuestadora_id')
        ->where('encuestas_estados.estado_id',$id_estado)
        ->where('e.nombre',$encuestadora)
        ->groupBY('fecha')
        ->orderBy('fecha', 'asc')
        ->get();

        foreach ($fechasDatos as $key => $fechaE) {

            $nuevaF=strftime("%b'%y", strtotime($fechaE->fecha));
            $fechaSinPunto = str_replace (".",' ',$nuevaF);
            array_push($fechas,strtoupper ($fechaSinPunto));
        }

        foreach ($partidos as  $partido) {

            $estimaciones= EncuestaEstado::select('encuestas_estados.id','encuestas_estados.fecha','pp.abreviacion','encuestas_estados.porcentaje_votos as porcentaje','pp.color')
            ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
             ->join('encuestadoras as e','e.id','encuestas_estados.encuestadora_id')
            ->where('encuestas_estados.estado_id',$id_estado)
            ->where('e.nombre',$encuestadora)
            ->where('encuestas_estados.partido_politico_id',$partido->id)
            ->get();



            if( count($estimaciones) >0 ){
                $datosEstimacion=array();

                foreach( $fechasDatos as $key => $fechaG){

                    $estimaciones= EncuestaEstado::select('encuestas_estados.id','encuestas_estados.fecha','pp.abreviacion','encuestas_estados.porcentaje_votos as porcentaje','pp.color')
                    ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
                     ->join('encuestadoras as e','e.id','encuestas_estados.encuestadora_id')
                    ->where('encuestas_estados.estado_id',$id_estado)
                    ->where('e.nombre',$encuestadora)
                    ->where('encuestas_estados.partido_politico_id',$partido->id)
                    ->where('encuestas_estados.fecha',$fechaG->fecha)
                    ->orderBy('fecha', 'asc')
                    ->first();

                    if($estimaciones){
                        array_push($datosEstimacion,floatval(number_format($estimaciones->porcentaje,1)));

                    }else{
                        array_push($datosEstimacion,'');
                    }

                    $obj = (object) array(
                        'nombre'     => $partido->abreviacion,
                        'promedios'  => $datosEstimacion,
                        'color'      => $partido->color
                    );

                }

                array_push($arrayNecesarioLineal,$obj);

            }

        }


        foreach ($partidos as  $partido) {



            $estimaciones= EncuestaEstado::select('encuestas_estados.id','encuestas_estados.fecha','pp.abreviacion','encuestas_estados.porcentaje_votos as porcentaje','pp.color')
            ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
             ->join('encuestadoras as e','e.id','encuestas_estados.encuestadora_id')
            ->where('encuestas_estados.estado_id',$id_estado)
            ->where('e.nombre',$encuestadora)
            ->where('encuestas_estados.partido_politico_id',$partido->id)->get();

            $encuestadoras = EncuestaEstado::select('encuestas_estados.id','encuestas_estados.fecha','pp.abreviacion','encuestas_estados.porcentaje_votos as porcentaje','pp.color')
            ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
             ->join('encuestadoras as e','e.id','encuestas_estados.encuestadora_id')
            ->where('encuestas_estados.estado_id',$id_estado )
            ->where('e.nombre','!=',$encuestadora)
            ->where('encuestas_estados.partido_politico_id',$partido->id)->get();
            $encuestadorasArray=array();

            if( count($encuestadoras) >0 ){

                foreach ($encuestadoras as $j => $encuestadoraVar) {

                    foreach ($fechasDatos as $i => $estimacion) {

                        if($estimacion->fecha==$encuestadoraVar->fecha){
                            $auxiliar=[$i,floatval(number_format($encuestadoraVar->porcentaje,1))];
                            array_push($encuestadorasArray,$auxiliar);
                        }else{
                            $auxiliar=[];
                            array_push($estimacionArray,$auxiliar);
                        }

                    }

                }

                $obj2 = (object) array(
                    'estatus'  => $partido->abreviacion,
                    'porcentaje'  => $encuestadorasArray,
                    'color' => $partido->color
                );

                array_push($arrayNecesarioDispersion,$obj2);

            }

        }

        return response()->json([
            'lineal'           => $arrayNecesarioLineal,
            'dispersion'       => $arrayNecesarioDispersion,
            'fechasDispersion' => $fechas
            ]);

    }

    public function getPollofPollsEstado(Request $request)
    {
        setlocale(LC_ALL,"es_ES");
        $id_encuestadora    = $request->input('id_encuestadora');
        $id_estado          = $request->input('id_estado');

        $partidos= PartidoPolitico::All();

        $arrayDatosPartidos =array();
        $arrayDatosGrafica  =array();
        $fechas             =array();


        $fechasDatos = EncuestaEstado::select('encuestas_estados.fecha as fecha')
        ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
        ->where('encuestas_estados.estado_id',$id_estado )
        ->where('encuestas_estados.encuestadora_id',$id_encuestadora )
        ->groupBY('fecha')
        ->orderBy('fecha', 'asc')
        ->get();

        foreach ($fechasDatos as $key => $fechaE) {
            $nuevaF=strftime("%b'%y", strtotime($fechaE->fecha));
            $fechaSinPunto = str_replace (".",' ',$nuevaF);
            array_push($fechas,strtoupper ($fechaSinPunto));
        }


            foreach ($partidos as $key => $partido) {

                $datosEstados = EncuestaEstado::select('pp.nombre','encuestas_estados.porcentaje_votos as porcentaje','pp.color','encuestas_estados.fecha as fecha')
                ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
                ->where('encuestas_estados.estado_id',$id_estado )
                ->where('encuestas_estados.encuestadora_id',$id_encuestadora )
                ->where('encuestas_estados.partido_politico_id',$partido->id)
                ->orderBy('fecha', 'asc')
                ->get();

            if(count($datosEstados)>0){

                $auxiliar=array();

                foreach( $fechasDatos as $key => $fechaG){

                $datosEncuesta = EncuestaEstado::select('pp.nombre','encuestas_estados.porcentaje_votos as porcentaje','pp.color','encuestas_estados.fecha as fecha')
                ->join('partidos_politicos as pp','pp.id','encuestas_estados.partido_politico_id')
                ->where('encuestas_estados.estado_id',$id_estado )
                ->where('encuestas_estados.encuestadora_id',$id_encuestadora )
                ->where('encuestas_estados.partido_politico_id',$partido->id)
                ->where('encuestas_estados.fecha',$fechaG->fecha)
                ->orderBy('fecha', 'asc')
                ->first();

                if($datosEncuesta){
                   array_push($auxiliar,floatval(number_format($datosEncuesta->porcentaje,1)));

                    // array_push($auxiliar,floatval(number_format($datos->porcentaje,1)));
                    // $nuevaF=strftime("%b'%y", strtotime($fechaG->fecha));
                    // $fechaSinPunto = str_replace (".",' ',$nuevaF);
                    // array_push($fechas,strtoupper ($fechaSinPunto));

                }else{
                    array_push($auxiliar,'');
                }
                    $obj = (object) array(
                    'name' => $partido->abreviacion,
                    'data' => $auxiliar,
                    'color' => $partido->color
                );


             }


             array_push($arrayDatosPartidos,$obj);

          }

        }

        return response()->json([
            'polls'            => $arrayDatosPartidos,
            'fechasDispersion' => $fechas

            ]);

    }


    public function anios_elecciones(){
        $anios_elecciones  =  VotoCongreso::select('anio_eleccion','titulo','fecha')
        ->groupBy('titulo')
        ->where('titulo',"!=",'2021')
        ->orderBy('anio_eleccion', 'asc')->get();

        return response()->json([
            'anios_eleccion' => $anios_elecciones
            ]);
    }




    public function getTablaCapitales(Request $request)
    {

        $id_encuestadora    = $request->input('id_encuestadora');
        $id_estado          = $request->input('id_estado');

        $totalCa=count($registrosCa = EncuestaMunicipio::select('m.nombre')
        ->from('municipios as m','m.id','encuestas_municipios.municipio_id')
        ->where('m.estado_id',$id_estado)
        ->groupBy('estado_id')->get());


        $partidos           = PartidoPolitico::All();
        $auxiliar=array();
        $arrayDatosPartidos=array();
        $arrayDatosGrafica=array();
        $fechas          =array();
        foreach ($partidos as $key => $partido) {
            $auxiliar=array();
            $datosEncuesta = EncuestaMunicipio::select('encuestas_municipios.fecha as fecha','pp.abreviacion as nombre','encuestas_municipios.porcenjate_votos as porcentaje','pp.color','pp.logo')
            ->join('partidos_politicos as pp','pp.id','encuestas_municipios.partido_politico_id')
            ->join('municipios as m','m.id','encuestas_municipios.municipio_id')
            ->where('m.estado_id',$id_estado )
            ->where('encuestas_municipios.porcenjate_votos','>',0 )
            ->where('encuestas_municipios.encuestadora_id',$id_encuestadora )
            ->where('encuestas_municipios.partido_politico_id',$partido->id)->get();

            if(count($datosEncuesta)!=0){
                foreach($datosEncuesta as $key => $datos){
                    array_push($auxiliar,$datos->porcentaje);

                    $nuevaF=strftime("%b'%y", strtotime($datos->fecha));
                    $fechaSinPunto = str_replace (".",' ',$nuevaF);
                    array_push($fechas,strtoupper ($fechaSinPunto));
                }


                 array_push($arrayDatosGrafica,$auxiliar);
                    $obj = (object) array(
                        'name'  => $partido->abreviacion,
                        'data'  => $auxiliar,
                        'color' => $partido->color
                    );
                 array_push($arrayDatosPartidos,$obj);
            }

            if($datosEncuesta!=null){
            array_push($auxiliar,$datosEncuesta);
            }
        }


        return response()->json([
            'polls'            => $arrayDatosPartidos,
            'fechasDispersion' => $fechas,
            'total'            => 0
            ]);

        // return response()->json([
        //     'polls'            => $arrayDatosPartidos,
        //     'fechasDispersion' => $fechas,
        //     'total'            => $totalCa
        //     ]);
    }

    public function getTablaAlcaldia(Request $request)
    {

        $id_encuestadora    = $request->input('id_encuestadora');
        $id_municipio       = $request->input('id_municipio');


        $partidos           = PartidoPolitico::All();
        $auxiliar=array();
        $arrayDatosPartidos=array();
        $arrayDatosGrafica=array();
        $fechas          =array();

        $fechasDatos = EncuestaMunicipio::select('encuestas_municipios.fecha as fecha')
            ->join('partidos_politicos as pp','pp.id','encuestas_municipios.partido_politico_id')
            ->where('encuestas_municipios.municipio_id',$id_municipio )
            ->where('encuestas_municipios.porcenjate_votos','>',0 )
            ->where('encuestas_municipios.encuestadora_id',$id_encuestadora )
            ->groupBY('fecha')
            ->orderBy('fecha', 'asc')
            ->get();

            foreach ($fechasDatos as $key => $fechaF) {
                $nuevaF=strftime("%b'%y", strtotime($fechaF->fecha));
                $fechaSinPunto = str_replace (".",' ',$nuevaF);
                array_push($fechas,strtoupper ($fechaSinPunto));
            }



        foreach ($partidos as $key => $partido) {

            $datosMunicipio = EncuestaMunicipio::select('encuestas_municipios.fecha as fecha','pp.abreviacion as nombre','encuestas_municipios.porcenjate_votos as porcentaje','pp.color','pp.logo')
            ->join('partidos_politicos as pp','pp.id','encuestas_municipios.partido_politico_id')
            ->where('encuestas_municipios.municipio_id',$id_municipio )
            ->where('encuestas_municipios.porcenjate_votos','>',0 )
            ->where('encuestas_municipios.encuestadora_id',$id_encuestadora )
            ->where('encuestas_municipios.partido_politico_id',$partido->id)->get();

            if(count($datosMunicipio)>0){

                $auxiliar=array();

                foreach( $fechasDatos as $key => $fechaG){

                    $datosEncuesta = EncuestaMunicipio::select('encuestas_municipios.fecha as fecha','pp.abreviacion as nombre','encuestas_municipios.porcenjate_votos as porcentaje','pp.color','pp.logo')
                    ->join('partidos_politicos as pp','pp.id','encuestas_municipios.partido_politico_id')
                    ->where('encuestas_municipios.municipio_id',$id_municipio )
                    ->where('encuestas_municipios.porcenjate_votos','>',0 )
                    ->where('encuestas_municipios.encuestadora_id',$id_encuestadora )
                    ->where('encuestas_municipios.partido_politico_id',$partido->id)
                    ->where('encuestas_municipios.fecha',$fechaG->fecha )
                    ->orderBy('fecha', 'asc')
                    ->first();

                    if($datosEncuesta){
                        array_push($auxiliar,floatval(number_format($datosEncuesta->porcentaje,1)));

                        // $nuevaF=strftime("%b'%y", strtotime($fechaG->fecha));
                        // $fechaSinPunto = str_replace (".",' ',$nuevaF);
                        // array_push($fechas,strtoupper ($fechaSinPunto));
                    }else{
                        array_push($auxiliar,'');
                    }

                    $obj = (object) array(
                        'name' => $partido->abreviacion,
                        'data' => $auxiliar,
                        'color' => $partido->color
                    );


                }

                array_push($arrayDatosPartidos,$obj);
            }

            // if($datosEncuesta!=null){
            // array_push($auxiliar,$datosEncuesta);
            // }
        }


        return response()->json([
            'polls'            => $arrayDatosPartidos,
            'fechasDispersion' => $fechas
            ]);

    }


    public function getGraficaBarrasCapital(Request $request){

        $id_estado    = $request->input('id_estado');

        $referencia  = VotoMunicipio::select('tg.referencia')
        ->join('municipios as m','m.id','votos_municipios.municipio_id')
        ->join('titulos_graficas as tg','tg.id','m.titulo_grafica_id')
        ->where('m.estado_id',$id_estado)->first();


        $fechaMasActual  = DB::table('votos_municipios')
        ->join('municipios as m','m.id','votos_municipios.municipio_id')
        ->where('m.estado_id',$id_estado)->get()
        ->max('fecha');


        $votos  = VotoMunicipio::select('votos_municipios.fecha','pp.abreviacion','votos_municipios.porcenjate_votos', 'pp.color','pp.logo')
        ->join('partidos_politicos as pp','pp.id','votos_municipios.partido_politico_id')
        ->join('municipios as m','m.id','votos_municipios.municipio_id')
        ->where('votos_municipios.porcenjate_votos','>',0 )
        ->where('votos_municipios.fecha',$fechaMasActual)
        ->where('m.estado_id',$id_estado)
        ->get();

        $candidatos = [];
        if(in_array($id_estado,[14,19]))
            $candidatos=Candidato::select('candidatos.nombre','candidatos.foto','pp.logo','pp.abreviacion')
            ->join('partidos_politicos as pp', 'pp.id' ,'candidatos.partido_politico_id')
            ->where('capital_id', $id_estado)
            ->where('anio_eleccion',date("Y"))
            ->get();

        $cand = [];
        foreach ($candidatos as $key => $c)
            if(!array_key_exists($c->abreviacion,$cand))
                $cand[$c->abreviacion] = [
                    "foto" => $c->foto,
                    "nombre" => $c->nombre."<br>".$c->abreviacion
                ];

        foreach ($votos as $key => $v)
            if (array_key_exists($v->abreviacion,$cand)){
                $v->logo = $cand[$v->abreviacion]["foto"];
                $v->abreviacion = $cand[$v->abreviacion]["nombre"];
            }

           return response()->json([
              'votos'  => $votos,
              'referencia' => $referencia,
          ]);

      }



    public function encuestadorasMunicipios(Request $request){

        $id_municipio          = $request->input('id_municipio');

        $encuestadoras = EncuestaMunicipio::select('e.id','e.nombre')
        ->join('encuestadoras as e','e.id','encuestas_municipios.encuestadora_id')
        ->where('encuestas_municipios.porcenjate_votos','>',0)
        ->where('e.nombre','!=','estimacion')
        // ->where('e.nombre','!=','Upax')
        ->where('encuestas_municipios.municipio_id',$id_municipio )
        ->groupBy('nombre')->get();

        return response()->json([
            'encuestadoras' => $encuestadoras
            ]);
    }


    public function encuestadorasAprobacion(){

        $encuestadoras  =  EncuestaAprobacion::select('e.id','e.nombre')
        ->join('encuestadoras as e','e.id','encuestas_aprobaciones.encuestadora_id')
        ->orderBy('e.nombre','desc')
        // ->where('e.nombre','!=','Upax')
        ->groupBy('nombre')->get();

        return response()->json([
            'encuestadoras' => $encuestadoras
            ]);
    }

    public function encuestadorasEstados(Request $request){

        $id_estado          = $request->input('id_estado');

        $encuestadoras  =  EncuestaEstado::select('e.id','e.nombre')
            ->join('encuestadoras as e','e.id','encuestas_estados.encuestadora_id')
            ->where('encuestas_estados.estado_id',$id_estado)
            ->where('e.nombre','!=','estimacion')
            // ->where('e.nombre','!=','Upax')
            ->groupBy('nombre')
            ->where('encuestas_estados.porcentaje_votos','>',0)
            ->orderByRaw('FIELD(e.nombre,"Demoscopia Digital")desc')
            ->get();

        return response()->json([
            'encuestadoras' => $encuestadoras
            ]);
    }

    public function encuestadorasCamara(){

        $encuestadoras  =  EncuestaCongreso::select('e.id','e.nombre')
        ->join('encuestadoras as e','e.id','encuestas_congresos.encuestadora_id')
        ->where('e.nombre','!=','estimacion')
        // ->where('e.nombre','!=','Upax')
        ->orderByRaw('FIELD(e.nombre,"Upax")desc')
        ->groupBy('nombre')->get();

        return response()->json([
            'encuestadoras' => $encuestadoras
            ]);
    }



    // public function getTablaAlcaldia(Request $request)
    // {
    //     $id_encuestadora    = $request->input('id_encuestadora');
    //     $id_municipio       = $request->input('id_municipio');

    //     $partidos           = PartidoPolitico::All();
    //     $auxiliar=array();
    //     foreach ($partidos as $key => $partido) {


    //         $datosEncuesta = EncuestaMunicipio::select('pp.abreviacion as nombre','encuestas_municipios.porcenjate_votos as porcentaje','pp.color','pp.logo')
    //         ->join('partidos_politicos as pp','pp.id','encuestas_municipios.partido_politico_id')
    //         ->where('encuestas_municipios.municipio_id',$id_municipio )
    //         ->where('encuestas_municipios.porcenjate_votos','>',0 )
    //         ->where('encuestas_municipios.encuestadora_id',$id_encuestadora )
    //         ->where('encuestas_municipios.partido_politico_id',$partido->id)->first();

    //         if($datosEncuesta!=null){
    //         array_push($auxiliar,$datosEncuesta);
    //         }
    //     }

    //     $fecha = EncuestaMunicipio::select(DB::raw('DATE_FORMAT(encuestas_municipios.fecha, "%m-%Y") as fecha'))
    //     ->join('partidos_politicos as pp','pp.id','encuestas_municipios.partido_politico_id')
    //     ->where('encuestas_municipios.municipio_id',$id_municipio )
    //     ->where('encuestas_municipios.porcenjate_votos','>',0 )
    //     ->where('encuestas_municipios.encuestadora_id',$id_encuestadora )
    //     ->groupBy('encuestas_municipios.fecha')->first();

    //     return response()->json([
    //         'auxiliar' => $auxiliar,
    //         'fecha'  => $fecha
    //         ]);

    // }

    // public function getTablaCapitales(Request $request)
    // {
    //     $id_encuestadora    = $request->input('id_encuestadora');
    //     $id_estado          = $request->input('id_estado');


    //     $partidos           = PartidoPolitico::All();
    //     $auxiliar=array();
    //     foreach ($partidos as $key => $partido) {


    //         $datosEncuesta = EncuestaMunicipio::select('pp.abreviacion as nombre','encuestas_municipios.porcenjate_votos as porcentaje','pp.color','pp.logo')
    //         ->join('partidos_politicos as pp','pp.id','encuestas_municipios.partido_politico_id')
    //         ->join('municipios as m','m.id','encuestas_municipios.municipio_id')
    //         ->where('m.estado_id',$id_estado )
    //         ->where('encuestas_municipios.porcenjate_votos','>',0 )
    //         ->where('encuestas_municipios.encuestadora_id',$id_encuestadora )
    //         ->where('encuestas_municipios.partido_politico_id',$partido->id)->first();

    //         if($datosEncuesta!=null){
    //         array_push($auxiliar,$datosEncuesta);
    //         }
    //     }

    //     $fecha = EncuestaMunicipio::select(DB::raw('DATE_FORMAT(encuestas_municipios.fecha, "%m-%Y") as fecha'))
    //     ->join('partidos_politicos as pp','pp.id','encuestas_municipios.partido_politico_id')
    //     ->join('municipios as m','m.id','encuestas_municipios.municipio_id')
    //     ->where('m.estado_id',$id_estado )
    //     ->where('encuestas_municipios.encuestadora_id',$id_encuestadora )
    //     ->groupBy('encuestas_municipios.fecha')->first();

    //     return response()->json([
    //         'auxiliar' => $auxiliar,
    //         'fecha'  => $fecha
    //         ]);

    // }









}
